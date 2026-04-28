from fastapi import FastAPI

app = FastAPI(title="Content Radar")


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
