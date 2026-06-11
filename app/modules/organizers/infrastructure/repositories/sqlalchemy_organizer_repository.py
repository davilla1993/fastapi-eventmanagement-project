from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.organizers.domain.entities.organizer import Organizer
from app.modules.organizers.domain.repositories.organizer_repository import (
    AbstractOrganizerRepository,
)


class SqlAlchemyOrganizerRepository(AbstractOrganizerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_public_id(self, public_id: UUID) -> Organizer | None:
        result = await self._session.execute(
            select(Organizer).where(
                Organizer.public_id == public_id, Organizer.deleted.is_(False)
            )
        )
        return result.scalar_one_or_none()

    async def find_by_email(self, email: str) -> Organizer | None:
        result = await self._session.execute(
            select(Organizer).where(
                Organizer.email == email, Organizer.deleted.is_(False)
            )
        )
        return result.scalar_one_or_none()

    async def find_all(self, offset: int, limit: int) -> tuple[list[Organizer], int]:
        base = select(Organizer).where(Organizer.deleted.is_(False))
        total_result = await self._session.execute(
            select(func.count()).select_from(base.subquery())
        )
        total: int = total_result.scalar_one()
        items_result = await self._session.execute(
            base.order_by(Organizer.name).offset(offset).limit(limit)
        )
        return list(items_result.scalars().all()), total

    async def save(self, organizer: Organizer) -> Organizer:
        self._session.add(organizer)
        await self._session.flush()
        await self._session.refresh(organizer)
        return organizer

    async def delete(self, organizer: Organizer) -> None:
        organizer.deleted = True
        self._session.add(organizer)
        await self._session.flush()
