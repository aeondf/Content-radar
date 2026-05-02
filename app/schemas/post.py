from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostResponse(BaseModel):
    """Public-facing Post representation."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    source_id: int
    external_id: str
    title: str
    url: str
    summary: str | None
    author: str | None
    published_at: datetime | None
    fetched_at: datetime
    created_at: datetime


class PostListResponse(BaseModel):
    """Paginated list of posts."""

    items: list[PostResponse]
    total: int
    limit: int
    offset: int
