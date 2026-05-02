from dataclasses import dataclass
from datetime import UTC, datetime

import feedparser


@dataclass(frozen=True)
class ParsedPost:
    external_id: str
    title: str
    url: str
    summary: str | None
    author: str | None
    published_at: datetime | None


def parse_rss(xml: str) -> list[ParsedPost]:
    """Parse RSS/Atom XML into a list of ParsedPost DTOs."""
    feed = feedparser.parse(xml)
    posts: list[ParsedPost] = []

    for entry in feed.entries:
        external_id_raw = getattr(entry, "id", None) or getattr(entry, "link", "")
        if not external_id_raw:
            continue
        external_id = str(external_id_raw)

        published_at: datetime | None = None
        if parsed := getattr(entry, "published_parsed", None):
            published_at = datetime(
                parsed.tm_year,
                parsed.tm_mon,
                parsed.tm_mday,
                parsed.tm_hour,
                parsed.tm_min,
                parsed.tm_sec,
                tzinfo=UTC,
            )

        summary = getattr(entry, "summary", None)
        author = getattr(entry, "author", None)

        posts.append(
            ParsedPost(
                external_id=external_id,
                title=str(getattr(entry, "title", "(no title)")),
                url=str(getattr(entry, "link", "")),
                summary=str(summary) if summary is not None else None,
                author=str(author) if author is not None else None,
                published_at=published_at,
            )
        )

    return posts
