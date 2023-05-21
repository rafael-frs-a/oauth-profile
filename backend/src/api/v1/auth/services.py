import uuid
import typing
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from src.api import utils
from src.api.schemas import ApiError
from src.api.v1.auth.enums import TokenType
from . import config, clients, schemas, stores


class AuthService:
    def __init__(self) -> None:
        self.auth0_client = clients.Auth0Client()
        self.store = stores.AuthStore()

    def make_authorize_response(
        self,
        authorize_request: schemas.AuthorizeRequest
    ) -> schemas.AuthorizeResponse:
        nonce_payload = {
            'id': str(uuid.uuid4())
        }

        nonce = utils.make_app_token(nonce_payload)
        authorization = self.auth0_client.get_authorization_data(nonce, authorize_request)
        response = schemas.AuthorizeResponse(data=authorization)
        return response

    def generate_credentials(self, user_id: typing.Optional[int]) -> schemas.AuthenticationCredentials:
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=config.ACCESS_TOKEN_EXP_SECONDS),
            'type': TokenType.ACCESS_TOKEN.name,
        }

        access_token = utils.make_app_token(payload)
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=config.REFRESH_TOKEN_EXP_SECONDS),
            'type': TokenType.REFRESH_TOKEN.name,
        }

        refresh_token = utils.make_app_token(payload)
        return schemas.AuthenticationCredentials(
            accessToken=access_token,
            refreshToken=refresh_token
        )

    async def login(
        self,
        login_request: schemas.LoginRequest
    ) -> schemas.LoginResponse:
        nonce_validation_result = utils.decode_app_token(login_request.nonce)

        if not nonce_validation_result.success:
            return schemas.LoginResponse(errors=nonce_validation_result.errors)

        client = clients.Auth0Client()
        client_result = await client.authenticate(login_request)

        if not client_result.success:
            return schemas.LoginResponse(errors=client_result.errors)

        if not client_result.data or not client_result.data.userInfo.get('email'):
            error = ApiError(
                message='Authentication method not supported',
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
            return schemas.LoginResponse(errors=[error])

        auth0_credentials = client_result.data
        email = auth0_credentials.userInfo['email']
        user = await self.store.upsert_user(email, auth0_credentials)
        credentials = self.generate_credentials(user.id)
        return schemas.LoginResponse(data=credentials)

    def refresh_token(
        self,
        refresh_token_requset: schemas.RefreshTokenRequest
    ) -> schemas.RefreshTokenResponse:
        decode_result = utils.decode_app_token(refresh_token_requset.refreshToken)

        if not decode_result.success:
            return schemas.RefreshTokenResponse(errors=decode_result.errors)

        token = decode_result.data

        if not token or token['type'] != TokenType.REFRESH_TOKEN.name:
            error = ApiError(
                message='Invalid token received',
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
            return schemas.RefreshTokenResponse(errors=[error])

        user_id = token.get('user_id')
        credentials = self.generate_credentials(user_id)
        return schemas.RefreshTokenResponse(data=credentials)


class AccessTokenValidator(HTTPBearer):
    def __init__(self) -> None:
        super().__init__(auto_error=False)

    async def __call__(self, request: Request) -> schemas.AuthenticatedUser:  # type: ignore[override]
        credentials = await super().__call__(request)

        if not credentials:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        decode_result = utils.decode_app_token(credentials.credentials)

        if decode_result.errors:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=decode_result.errors[0].message
            )

        access_token = decode_result.data

        if not access_token or access_token.get('type') != TokenType.ACCESS_TOKEN.name:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return schemas.AuthenticatedUser(id=access_token.get('user_id'))
