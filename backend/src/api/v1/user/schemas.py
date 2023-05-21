import typing
from datetime import datetime
from pydantic import BaseModel
from src.api.schemas import ApiResponse


class UserProfile(BaseModel):
    email: str
    compiledProfile: dict[typing.Any, typing.Any]
    history: list[typing.Any]
    createdAt: datetime
    updatedAt: datetime


class ProfileResponse(ApiResponse[UserProfile]):
    ...
