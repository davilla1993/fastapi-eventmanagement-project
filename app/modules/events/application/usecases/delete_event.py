from uuid import UUID

from app.infrastructure.audit.audit_service import AuditService
from app.modules.events.domain.exceptions.event_exceptions import EventNotFoundException
from app.modules.events.domain.repositories.event_repository import (
    AbstractEventRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork


class DeleteEventUseCase:
    def __init__(
        self,
        repository: AbstractEventRepository,
        uow: UnitOfWork,
        audit: AuditService,
    ) -> None:
        self._repository = repository
        self._uow = uow
        self._audit = audit

    async def execute(self, public_id: UUID, actor_public_id: UUID) -> None:
        event = await self._repository.find_by_public_id(public_id)
        if not event:
            raise EventNotFoundException(str(public_id))

        event.deleted_by = actor_public_id
        await self._repository.delete(event)
        await self._audit.log(
            entity_type="event",
            entity_public_id=public_id,
            action="deleted",
            actor_public_id=actor_public_id,
        )
        await self._uow.commit()