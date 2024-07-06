from fastapi import FastAPI

from server.core.config import settings

app = FastAPI()


@app.get("/health")
async def health():
    print(settings)
    return {"status": "ok"}
