from uuid import UUID

from app.infrastructure.audit.audit_service import AuditService
from app.modules.venues.domain.exceptions.venue_exceptions import VenueNotFoundException
from app.modules.venues.domain.repositories.venue_repository import (
    AbstractVenueRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork


class DeleteVenueUseCase:
    def __init__(
        self, repository: AbstractVenueRepository, uow: UnitOfWork, audit: AuditService
    ) -> None:
        self._repository = repository
        self._uow = uow
        self._audit = audit

    async def execute(self, public_id: UUID, actor_public_id: UUID) -> None:
        venue = await self._repository.find_by_public_id(public_id)
        if not venue:
            raise VenueNotFoundException(str(public_id))

        venue.deleted_by = actor_public_id
        await self._repository.delete(venue)
        await self._audit.log(
            entity_type="venue",
            entity_public_id=public_id,
            action="deleted",
            actor_public_id=actor_public_id,
        )
        await self._uow.commit()