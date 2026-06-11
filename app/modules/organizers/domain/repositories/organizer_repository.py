from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.organizers.domain.entities.organizer import Organizer


class AbstractOrganizerRepository(ABC):
    @abstractmethod
    async def find_by_public_id(self, public_id: UUID) -> Organizer | None: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> Organizer | None: ...

    @abstractmethod
    async def find_all(
        self, offset: int, limit: int
    ) -> tuple[list[Organizer], int]: ...

    @abstractmethod
    async def save(self, organizer: Organizer) -> Organizer: ...

    @abstractmethod
    async def delete(self, organizer: Organizer) -> None: ...
