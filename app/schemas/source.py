from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.source import SourceType


class SourceResponse(BaseModel):
    """Public-facing Source representation."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: SourceType
    url: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
