from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db

app = FastAPI(title=settings.app_name)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "env": settings.env}


@app.get("/health/db")
async def health_db_check(db: Annotated[AsyncSession, Depends(get_db)]) -> dict[str, str | int]:
    result = await db.execute(text("SELECT 1"))
    value = result.scalar_one()
    return {"status": "ok", "result": value}
