import typing
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db import engine
from src.db.models.user import User
from src.api.v1.auth import schemas as auth_schemas


class UserStore:
    async def _get_user(
        self,
        user: auth_schemas.AuthenticatedUser,
        session: AsyncSession
    ) -> typing.Optional[User]:
        statement = select(User).where(User.id == user.id)
        results = await session.execute(statement)
        return results.scalar_one_or_none()

    async def get_user(
        self,
        user: auth_schemas.AuthenticatedUser
    ) -> typing.Optional[User]:
        async with engine.get_async_session() as session:
            return await self._get_user(user, session)
