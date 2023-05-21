import copy
import typing
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db import engine
from src.db.models.user import User, Auth0Credentials
from . import config, schemas


class AuthStore:
    async def _get_user(self, email: str, session: AsyncSession) -> typing.Optional[User]:
        statement = select(
            User
        ).where(
            User.email == email
        ).options(
            selectinload(User.auth0_credentials)
        )

        results = await session.execute(statement)
        return results.scalar_one_or_none()

    def _upsert_auth0_credentials(self, user: User, credentials: schemas.Auth0Credentials) -> User:
        if not user.auth0_credentials:
            user.auth0_credentials = Auth0Credentials()

        user.auth0_credentials.access_token = credentials.accessToken
        return user

    async def _upsert_user(
        self,
        email: str,
        user_info: schemas.UserInfo,
        session: AsyncSession
    ) -> User:
        email = email.lower()
        user = await self._get_user(email, session)

        if not user:
            user = User()
            user.email = email

        user.compiled_profile = copy.deepcopy(user.compiled_profile)
        user.profile_history = copy.deepcopy(user.profile_history)
        user.compiled_profile.update(user_info.userInfo)
        user.profile_history.insert(0, user_info.userInfo)
        user.profile_history = user.profile_history[:config.MAX_LENGTH_PROFILE_HISTORY]

        if isinstance(user_info, schemas.Auth0Credentials):
            user = self._upsert_auth0_credentials(user, user_info)

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return (await self._get_user(email, session)) or user

    async def upsert_user(self, email: str, user_info: schemas.UserInfo) -> User:
        async with engine.get_async_session() as session:
            return await self._upsert_user(email, user_info, session)
