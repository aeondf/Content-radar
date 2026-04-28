# Content Radar

LLM-агент, который агрегирует контент из RSS, Reddit, Hacker News, YouTube и других источников, и сам решает, что с ним делать: суммаризировать, фильтровать, искать связи между постами, копать глубже.

## Status

🚧 В активной разработке — этап 0 (project setup).

## Tech stack (планируется)

- **Backend:** Python 3.13, FastAPI, SQLAlchemy 2.0 (async), Alembic
- **DB:** PostgreSQL + pgvector
- **LLM:** Anthropic SDK (tool use)
- **Infra:** Docker Compose, Redis
- **Tooling:** uv, ruff, pre-commit, pytest

## Local setup

Требования: Python 3.13, [uv](https://docs.astral.sh/uv/), Docker.

```bash
# Установить зависимости (создаст .venv/ автоматически)
uv sync

# Поставить pre-commit хуки
uv run pre-commit install
```

## Roadmap

См. [ROADMAP.md](./ROADMAP.md) (TBD).
