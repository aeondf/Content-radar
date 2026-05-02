import asyncio
from dataclasses import dataclass

import typer
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.source import Source, SourceType


@dataclass(frozen=True)
class SourceSeed:
    name: str
    type: SourceType
    url: str


STARTER_SOURCES: list[SourceSeed] = [
    SourceSeed(
        name="Hacker News",
        type=SourceType.RSS,
        url="https://hnrss.org/frontpage",
    ),
    SourceSeed(
        name="Lobsters",
        type=SourceType.RSS,
        url="https://lobste.rs/rss",
    ),
    SourceSeed(
        name="The Verge",
        type=SourceType.RSS,
        url="https://www.theverge.com/rss/index.xml",
    ),
]


async def _seed_sources() -> tuple[int, int]:
    """Returns (added, skipped)."""
    added = 0
    skipped = 0
    async with SessionLocal() as session:
        for seed in STARTER_SOURCES:
            existing = await session.scalar(select(Source).where(Source.name == seed.name))
            if existing is not None:
                skipped += 1
                continue
            session.add(Source(name=seed.name, type=seed.type, url=seed.url))
            added += 1
        await session.commit()
    return added, skipped


def seed_sources() -> None:
    """Seed starter content sources into the database (idempotent)."""
    added, skipped = asyncio.run(_seed_sources())
    typer.echo(f"Seeded sources: {added} added, {skipped} already existed.")
