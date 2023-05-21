from fastapi import APIRouter
from . import schemas

router = APIRouter(tags=['Meta'])


@router.get('/health-check')
async def health_check() -> schemas.ApiResponse[None]:
    return schemas.ApiResponse()
