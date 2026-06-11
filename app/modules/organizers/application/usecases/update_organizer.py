from uuid import UUID

from app.modules.iam.domain.entities.user import UserRole
from app.modules.organizers.api.dto.requests.organizer_requests import OrganizerUpdate
from app.modules.organizers.api.dto.responses.organizer_responses import (
    OrganizerReadDetail,
)
from app.modules.organizers.application.mappers.organizer_mapper import OrganizerMapper
from app.modules.organizers.domain.exceptions.organizer_exceptions import (
    OrganizerEmailAlreadyExistsException,
    OrganizerNotFoundException,
)
from app.modules.organizers.domain.repositories.organizer_repository import (
    AbstractOrganizerRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork
from app.shared.exceptions.base import ForbiddenException


class UpdateOrganizerUseCase:
    def __init__(
        self, repository: AbstractOrganizerRepository, uow: UnitOfWork
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def execute(
        self,
        public_id: UUID,
        request: OrganizerUpdate,
        actor_public_id: UUID,
        actor_role: UserRole,
    ) -> OrganizerReadDetail:
        organizer = await self._repository.find_by_public_id(public_id)
        if not organizer:
            raise OrganizerNotFoundException(str(public_id))

        if actor_role != UserRole.ADMIN and organizer.user_public_id != actor_public_id:
            raise ForbiddenException()

        if request.email and request.email != organizer.email:
            if await self._repository.find_by_email(request.email):
                raise OrganizerEmailAlreadyExistsException(request.email)
            organizer.email = request.email

        if request.name is not None:
            organizer.name = request.name
        if request.telephone is not None:
            organizer.telephone = str(request.telephone)
        if request.website is not None:
            organizer.website = request.website
        if request.description is not None:
            organizer.description = request.description

        organizer.updated_by = actor_public_id
        saved = await self._repository.save(organizer)
        await self._uow.commit()
        return OrganizerMapper.to_detail(saved)
