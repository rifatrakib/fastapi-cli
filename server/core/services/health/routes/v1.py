from fastapi import APIRouter

from server.core.config import settings
from server.core.enums import Tags

from ..schemas.responses import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=[Tags.HEALTH_CHECK],
)


@router.get(
    "",
    summary="Health check",
    response_model=HealthResponse,
)
async def health_check():
    return settings
