from fastapi import APIRouter, Body, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.api.error.schemas import INVALID_DATA_RESPONSE
from . import schemas, services

router = APIRouter(prefix='/auth', tags=['Auth'])

authorize_responses = {
    status.HTTP_200_OK: {
        'model': schemas.AuthorizeResponse,
    }
} | INVALID_DATA_RESPONSE

login_responses = {
    status.HTTP_200_OK: {
        'model': schemas.LoginResponse,
    }
} | INVALID_DATA_RESPONSE

refresh_token_responses = {
    status.HTTP_200_OK: {
        'model': schemas.RefreshTokenResponse,
    }
} | INVALID_DATA_RESPONSE


@router.post('/authorize', responses=authorize_responses)
async def authorize(
    authorize_request: schemas.AuthorizeRequest = Body()
) -> Response:
    service = services.AuthService()
    response = service.make_authorize_response(authorize_request)
    status_code = status.HTTP_200_OK if response.success else status.HTTP_422_UNPROCESSABLE_ENTITY
    return JSONResponse(
        content=jsonable_encoder(response),
        status_code=status_code
    )


@router.post('/login', responses=login_responses)
async def login(
    login_request: schemas.LoginRequest = Body()
) -> Response:
    service = services.AuthService()
    response = await service.login(login_request)
    status_code = status.HTTP_200_OK if response.success else status.HTTP_422_UNPROCESSABLE_ENTITY
    return JSONResponse(
        content=jsonable_encoder(response),
        status_code=status_code
    )


@router.post('/refresh-token', responses=refresh_token_responses)
async def refresh_token(
    refresh_token_request: schemas.RefreshTokenRequest = Body()
) -> Response:
    service = services.AuthService()
    response = service.refresh_token(refresh_token_request)
    status_code = status.HTTP_200_OK if response.success else status.HTTP_422_UNPROCESSABLE_ENTITY
    return JSONResponse(
        content=jsonable_encoder(response),
        status_code=status_code
    )
