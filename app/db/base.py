from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models AFTER Base is defined to register them in Base.metadata.
# This is intentionally at the bottom — needed for alembic autogenerate.
from app.models.source import Source  # noqa: F401, E402
