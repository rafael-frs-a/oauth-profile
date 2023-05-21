from fastapi import status
from src.api.schemas import ApiError
from src.api.v1.auth import schemas as auth_schemas
from . import schemas, stores


class UserService:
    def __init__(self) -> None:
        self.store = stores.UserStore()

    async def get_user_profile(
        self,
        authenticated_user: auth_schemas.AuthenticatedUser
    ) -> schemas.ProfileResponse:
        user = await self.store.get_user(authenticated_user)

        if not user:
            error = ApiError(
                message='User not found',
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
            return schemas.ProfileResponse(
                errors=[error]
            )

        user_profile = schemas.UserProfile(
            email=user.email,
            compiledProfile=user.compiled_profile,
            history=user.profile_history,
            createdAt=user.created_at,
            updatedAt=user.updated_at
        )

        return schemas.ProfileResponse(data=user_profile)
