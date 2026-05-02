import asyncio
import logging

import typer
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.source import Source
from app.services.fetcher import fetch_and_save

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


async def _fetch_all() -> None:
    async with SessionLocal() as session:
        sources = (await session.scalars(select(Source).where(Source.is_active.is_(True)))).all()
        if not sources:
            typer.echo("No active sources. Run `seed-sources` first.")
            return

        for source in sources:
            try:
                added, skipped = await fetch_and_save(session, source)
                typer.echo(f"  {source.name}: +{added} new, {skipped} dup")
            except Exception as e:
                typer.echo(f"  {source.name}: ERROR — {e}")


def fetch_all() -> None:
    """Fetch posts from all active sources."""
    asyncio.run(_fetch_all())
