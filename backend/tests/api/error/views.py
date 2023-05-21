from fastapi import APIRouter, Depends
from src.api.schemas import ApiResponse
from src.api.error.handlers import TeapotException
from src.api.v1.auth import schemas as auth_schemas, services as auth_services

router = APIRouter(prefix='/error')


class TestException(Exception):
    ...


@router.get('/401', include_in_schema=False)
async def authentication_error(
    user: auth_schemas.AuthenticatedUser = Depends(auth_services.AccessTokenValidator())
) -> ApiResponse[None]:
    return ApiResponse()


@router.get('/405', include_in_schema=False)
async def method_not_allowed() -> ApiResponse[None]:
    return ApiResponse()


@router.get('/418', include_in_schema=False)
async def teapot_error() -> None:
    raise TeapotException('I\'m a teapot')


@router.get('/500', include_in_schema=False)
async def server_error() -> None:
    raise TestException('Test server error')
