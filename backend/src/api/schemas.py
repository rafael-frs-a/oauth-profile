import typing
from datetime import datetime
from pydantic import root_validator, BaseModel
from pydantic.generics import GenericModel

TData = typing.TypeVar('TData')
OpenApiResponse = dict[typing.Union[int, str], dict[str, typing.Any]]


class ApiError(BaseModel):
    message: str
    pointer: typing.Optional[str] = None
    header: typing.Optional[str] = None
    status: int


class ApiResponse(GenericModel, typing.Generic[TData]):
    success: bool = True
    data: typing.Optional[TData] = None
    errors: typing.Optional[list[ApiError]] = None

    @root_validator
    def make_response(cls, values: dict[str, typing.Any]) -> dict[str, typing.Any]:
        values['success'] = not values.get('errors')
        return values

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat('T') + 'Z'
        }


class ApiErrorResponse(ApiResponse[None]):
    success: bool = False
