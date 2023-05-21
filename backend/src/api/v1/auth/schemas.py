import typing
from pydantic import BaseModel, validator
from src.api import utils
from src.api.schemas import ApiResponse


class AuthorizeRequest(BaseModel):
    callbackUrl: str
    redirectAfterLogoutUrl: typing.Optional[str]

    @validator('callbackUrl')
    def validate_callback_url(cls, v: str) -> str:
        return utils.validate_url(v)

    @validator('redirectAfterLogoutUrl')
    def validate_redirect_logout_url(cls, v: typing.Optional[str]) -> typing.Optional[str]:
        if v is None:
            return v

        return utils.validate_url(v)


class Authorization(BaseModel):
    authorizationUrl: str
    logoutUrl: str
    nonce: str

    @validator('authorizationUrl')
    def validate_authorization_url(cls, v: str) -> str:
        return utils.validate_url(v)

    @validator('logoutUrl')
    def validate_logout_url(cls, v: str) -> str:
        return utils.validate_url(v)


class AuthorizeResponse(ApiResponse[Authorization]):
    ...


class LoginRequest(BaseModel):
    code: str
    callbackUrl: str
    nonce: str

    @validator('callbackUrl')
    def validate_callback_url(cls, v: str) -> str:
        return utils.validate_url(v)


class UserInfo(BaseModel):
    userInfo: dict[str, typing.Any]


class Auth0Credentials(UserInfo):
    accessToken: str


class Auth0Response(ApiResponse[Auth0Credentials]):
    ...


class AuthenticationCredentials(BaseModel):
    accessToken: str
    refreshToken: str


class LoginResponse(ApiResponse[AuthenticationCredentials]):
    ...


class RefreshTokenRequest(BaseModel):
    refreshToken: str


class RefreshTokenResponse(ApiResponse[AuthenticationCredentials]):
    ...


class AuthenticatedUser(BaseModel):
    id: typing.Optional[int]
