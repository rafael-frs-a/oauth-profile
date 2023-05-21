import jwt
import validators
import typing
from fastapi import status
from validators.utils import ValidationFailure
from src.api.schemas import ApiError
from . import config, schemas


def make_app_token(payload: dict[str, typing.Any]) -> str:
    return jwt.encode(
        payload,
        config.SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )


def decode_jwt_token(
    token: str,
    key: str = '',
    algorithms: list[str] | None = None,
    verify_signature: bool = True
) -> schemas.ApiResponse[dict[str, typing.Any]]:
    try:
        options = {'verify_signature': verify_signature}
        content = jwt.decode(token, key, algorithms=algorithms, options=options)
        return schemas.ApiResponse(data=content)
    except jwt.exceptions.ExpiredSignatureError:
        error = ApiError(message='Expired token', status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return schemas.ApiResponse(errors=[error])
    except jwt.exceptions.InvalidTokenError:
        error = ApiError(message='Invalid token', status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return schemas.ApiResponse(errors=[error])


def decode_app_token(
    token: str
) -> schemas.ApiResponse[dict[str, typing.Any]]:
    return decode_jwt_token(
        token,
        config.SECRET_KEY,
        [config.JWT_ALGORITHM],
    )


def validate_url(url: str) -> str:
    if config.FRONTEND_URL and url.startswith(config.FRONTEND_URL):
        return url

    validation_result = validators.url(url)

    if isinstance(validation_result, ValidationFailure):
        raise ValueError('Invalid URL')

    return url
