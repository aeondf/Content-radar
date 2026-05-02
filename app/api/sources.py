from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.source import Source
from app.schemas.source import SourceResponse

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("", response_model=list[SourceResponse])
async def list_sources(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[Source]:
    """List all content sources."""
    result = await db.scalars(select(Source).order_by(Source.id))
    return list(result)
