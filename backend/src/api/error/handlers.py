from fastapi import FastAPI, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from src.api.schemas import ApiResponse, ApiError, ApiErrorResponse


class TeapotException(Exception):
    ...


def init_errors(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ) -> JSONResponse:
        errors: list[ApiError] = []
        status_code = status.HTTP_400_BAD_REQUEST

        for error in exc.errors():
            msg = error.get('msg')
            loc = error.get('loc')

            if msg and loc:
                pointer = '/' + '/'.join(str(_) for _ in loc[1:])
                api_error = ApiError(message=msg, pointer=pointer, status=status_code)
                errors.append(api_error)

        api_response = ApiErrorResponse(errors=errors)
        return JSONResponse(
            content=jsonable_encoder(api_response),
            status_code=status_code
        )

    @app.exception_handler(TeapotException)
    async def teapot_handler(request: Request, exc: TeapotException) -> JSONResponse:
        api_response = ApiResponse[str](data='🍵')
        return JSONResponse(
            content=jsonable_encoder(api_response),
            status_code=status.HTTP_418_IM_A_TEAPOT
        )

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error = ApiError(message='Server error', status=status_code)
        api_response = ApiErrorResponse(errors=[error])
        return JSONResponse(
            content=jsonable_encoder(api_response),
            status_code=status_code
        )

    @app.exception_handler(status.HTTP_401_UNAUTHORIZED)
    async def unauthorized_handler(request: Request, exc: HTTPException) -> JSONResponse:
        status_code = status.HTTP_401_UNAUTHORIZED
        error = ApiError(
            message='Invalid or expired token',
            header='Authorization',
            status=status_code
        )
        api_response = ApiErrorResponse(errors=[error])
        return JSONResponse(
            content=jsonable_encoder(api_response),
            status_code=status_code
        )

    @app.exception_handler(status.HTTP_404_NOT_FOUND)
    async def not_found_handler(request: Request, exc: HTTPException) -> JSONResponse:
        status_code = status.HTTP_404_NOT_FOUND
        error = ApiError(message='Not found', status=status_code)
        api_response = ApiErrorResponse(errors=[error])
        return JSONResponse(
            content=jsonable_encoder(api_response),
            status_code=status_code
        )

    @app.exception_handler(status.HTTP_405_METHOD_NOT_ALLOWED)
    async def method_not_allowed_handler(request: Request, exc: HTTPException) -> JSONResponse:
        status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        error = ApiError(message='Method not allowed', status=status_code)
        api_response = ApiErrorResponse(errors=[error])
        return JSONResponse(
            content=jsonable_encoder(api_response),
            status_code=status_code
        )
