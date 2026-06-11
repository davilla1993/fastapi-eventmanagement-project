from uuid import UUID

from app.modules.organizers.api.dto.responses.organizer_responses import (
    OrganizerReadDetail,
)
from app.modules.organizers.application.mappers.organizer_mapper import OrganizerMapper
from app.modules.organizers.domain.exceptions.organizer_exceptions import (
    OrganizerNotFoundException,
)
from app.modules.organizers.domain.repositories.organizer_repository import (
    AbstractOrganizerRepository,
)


class GetOrganizerUseCase:
    def __init__(self, repository: AbstractOrganizerRepository) -> None:
        self._repository = repository

    async def execute(self, public_id: UUID) -> OrganizerReadDetail:
        organizer = await self._repository.find_by_public_id(public_id)
        if not organizer:
            raise OrganizerNotFoundException(str(public_id))
        return OrganizerMapper.to_detail(organizer)
