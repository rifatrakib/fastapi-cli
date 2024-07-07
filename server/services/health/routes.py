from fastapi import APIRouter

from server.core.enums import Tags

router = APIRouter(prefix="/health", tags=[Tags.HEALTH_CHECK])


@router.get("")
async def health_check():
    return {"status": "ok"}
