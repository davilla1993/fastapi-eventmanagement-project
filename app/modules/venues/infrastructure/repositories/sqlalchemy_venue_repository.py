from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.venues.domain.entities.venue import Venue
from app.modules.venues.domain.repositories.venue_repository import (
    AbstractVenueRepository,
)


class SqlAlchemyVenueRepository(AbstractVenueRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_public_id(self, public_id: UUID) -> Venue | None:
        result = await self._session.execute(
            select(Venue).where(Venue.public_id == public_id, Venue.deleted.is_(False))
        )
        return result.scalar_one_or_none()

    async def find_by_slug(self, slug: str) -> Venue | None:
        result = await self._session.execute(
            select(Venue).where(Venue.slug == slug, Venue.deleted.is_(False))
        )
        return result.scalar_one_or_none()

    async def find_all(
        self, offset: int, limit: int, city: str | None = None
    ) -> tuple[list[Venue], int]:
        base = select(Venue).where(Venue.deleted.is_(False))
        if city:
            base = base.where(Venue.city.ilike(f"%{city}%"))
        total_result = await self._session.execute(
            select(func.count()).select_from(base.subquery())
        )
        total: int = total_result.scalar_one()
        items_result = await self._session.execute(
            base.order_by(Venue.name).offset(offset).limit(limit)
        )
        return list(items_result.scalars().all()), total

    async def save(self, venue: Venue) -> Venue:
        self._session.add(venue)
        await self._session.flush()
        await self._session.refresh(venue)
        return venue

    async def delete(self, venue: Venue) -> None:
        venue.deleted = True
        self._session.add(venue)
        await self._session.flush()