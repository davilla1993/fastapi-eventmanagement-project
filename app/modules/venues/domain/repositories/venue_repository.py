from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.venues.domain.entities.venue import Venue


class AbstractVenueRepository(ABC):
    @abstractmethod
    async def find_by_public_id(self, public_id: UUID) -> Venue | None: ...

    @abstractmethod
    async def find_by_slug(self, slug: str) -> Venue | None: ...

    @abstractmethod
    async def find_all(
        self, offset: int, limit: int, city: str | None = None
    ) -> tuple[list[Venue], int]: ...

    @abstractmethod
    async def save(self, venue: Venue) -> Venue: ...

    @abstractmethod
    async def delete(self, venue: Venue) -> None: ...