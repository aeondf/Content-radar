from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.post import Post
from app.schemas.post import PostListResponse, PostResponse

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=PostListResponse)
async def list_posts(
    db: Annotated[AsyncSession, Depends(get_db)],
    source_id: Annotated[int | None, Query(description="Filter by source id")] = None,
    since: Annotated[
        datetime | None, Query(description="Only posts published at or after this datetime")
    ] = None,
    limit: Annotated[int, Query(ge=1, le=100, description="Page size, 1..100")] = 20,
    offset: Annotated[int, Query(ge=0, description="Skip this many records")] = 0,
) -> PostListResponse:
    """List posts with pagination and optional filters."""
    base = select(Post)
    if source_id is not None:
        base = base.where(Post.source_id == source_id)
    if since is not None:
        base = base.where(Post.published_at >= since)

    total = await db.scalar(select(func.count()).select_from(base.subquery())) or 0

    page = base.order_by(Post.published_at.desc().nullslast()).limit(limit).offset(offset)
    result = await db.scalars(page)
    items = [PostResponse.model_validate(p) for p in result]

    return PostListResponse(items=items, total=total, limit=limit, offset=offset)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Post:
    """Get a single post by id."""
    post = await db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
