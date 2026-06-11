from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.iam.domain.entities.user import User
from app.modules.iam.domain.repositories.user_repository import AbstractUserRepository


class SqlAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.email == email, User.deleted.is_(False))
        )
        return result.scalar_one_or_none()

    async def find_by_public_id(self, public_id: UUID) -> User | None:
        result = await self._session.execute(
            select(User).where(User.public_id == public_id, User.deleted.is_(False))
        )
        return result.scalar_one_or_none()

    async def save(self, user: User) -> User:
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)
        return user
