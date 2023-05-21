from fastapi import APIRouter, Response, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.api.error.schemas import INVALID_DATA_RESPONSE
from src.api.v1.auth import schemas as auth_schemas, services as auth_services
from . import schemas, services

router = APIRouter(prefix='/user', tags=['User'])

profile_responses = {
    status.HTTP_200_OK: {
        'model': schemas.ProfileResponse,
    }
} | INVALID_DATA_RESPONSE


@router.get('/profile', responses=profile_responses)
async def profile(
    user: auth_schemas.AuthenticatedUser = Depends(auth_services.AccessTokenValidator())
) -> Response:
    service = services.UserService()
    response = await service.get_user_profile(user)
    status_code = status.HTTP_200_OK if response.success else status.HTTP_422_UNPROCESSABLE_ENTITY
    return JSONResponse(
        content=jsonable_encoder(response),
        status_code=status_code
    )
