import logging
from collections.abc import Iterable

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.models.source import Source
from app.services.rss import ParsedPost, parse_rss

logger = logging.getLogger(__name__)


async def fetch_source(client: httpx.AsyncClient, source: Source) -> list[ParsedPost]:
    """Download a source's feed and parse it. Network only — no DB writes."""
    logger.info("Fetching %s (%s)", source.name, source.url)
    response = await client.get(source.url, timeout=30.0, follow_redirects=True)
    response.raise_for_status()
    return parse_rss(response.text)


async def save_posts(
    session: AsyncSession, source: Source, parsed_posts: Iterable[ParsedPost]
) -> tuple[int, int]:
    """Save parsed posts to DB with dedup. Returns (added, skipped)."""
    added = 0
    skipped = 0

    for parsed in parsed_posts:
        existing = await session.scalar(
            select(Post).where(
                Post.source_id == source.id,
                Post.external_id == parsed.external_id,
            )
        )
        if existing is not None:
            skipped += 1
            continue

        session.add(
            Post(
                source_id=source.id,
                external_id=parsed.external_id,
                title=parsed.title,
                url=parsed.url,
                summary=parsed.summary,
                author=parsed.author,
                published_at=parsed.published_at,
            )
        )
        added += 1

    await session.commit()
    return added, skipped


async def fetch_and_save(session: AsyncSession, source: Source) -> tuple[int, int]:
    """High-level: fetch one source and persist new posts."""
    async with httpx.AsyncClient(headers={"User-Agent": "content-radar/0.1"}) as client:
        parsed_posts = await fetch_source(client, source)
    return await save_posts(session, source, parsed_posts)
