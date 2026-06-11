from uuid import UUID

from app.modules.organizers.api.dto.requests.organizer_requests import OrganizerCreate
from app.modules.organizers.api.dto.responses.organizer_responses import (
    OrganizerReadDetail,
)
from app.modules.organizers.application.mappers.organizer_mapper import OrganizerMapper
from app.modules.organizers.domain.entities.organizer import Organizer
from app.modules.organizers.domain.exceptions.organizer_exceptions import (
    OrganizerEmailAlreadyExistsException,
)
from app.modules.organizers.domain.repositories.organizer_repository import (
    AbstractOrganizerRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork


class CreateOrganizerUseCase:
    def __init__(
        self, repository: AbstractOrganizerRepository, uow: UnitOfWork
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def execute(
        self, request: OrganizerCreate, actor_public_id: UUID
    ) -> OrganizerReadDetail:
        if await self._repository.find_by_email(request.email):
            raise OrganizerEmailAlreadyExistsException(request.email)

        organizer = Organizer(
            name=request.name,
            email=request.email,
            telephone=str(request.telephone) if request.telephone else None,
            website=request.website,
            description=request.description,
            user_public_id=actor_public_id,
            created_by=actor_public_id,
            updated_by=actor_public_id,
        )
        saved = await self._repository.save(organizer)
        await self._uow.commit()
        return OrganizerMapper.to_detail(saved)
