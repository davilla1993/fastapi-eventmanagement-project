from uuid import UUID

from app.modules.organizers.domain.exceptions.organizer_exceptions import (
    OrganizerNotFoundException,
)
from app.modules.organizers.domain.repositories.organizer_repository import (
    AbstractOrganizerRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork


class DeleteOrganizerUseCase:
    def __init__(
        self, repository: AbstractOrganizerRepository, uow: UnitOfWork
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def execute(self, public_id: UUID, actor_public_id: UUID) -> None:
        organizer = await self._repository.find_by_public_id(public_id)
        if not organizer:
            raise OrganizerNotFoundException(str(public_id))

        organizer.deleted_by = actor_public_id
        await self._repository.delete(organizer)
        await self._uow.commit()
