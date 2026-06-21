from fastapi import FastAPI

app = FastAPI(
    title="research-assistant",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict:
    """Liveness probe — returns 200 OK when the service is running."""
    return {"status": "ok"}
