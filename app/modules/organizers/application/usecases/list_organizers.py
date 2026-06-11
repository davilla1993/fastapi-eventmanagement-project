from app.modules.organizers.api.dto.responses.organizer_responses import OrganizerRead
from app.modules.organizers.application.mappers.organizer_mapper import OrganizerMapper
from app.modules.organizers.domain.repositories.organizer_repository import (
    AbstractOrganizerRepository,
)
from app.shared.pagination.schemas import PaginatedResponse, PaginationParams


class ListOrganizersUseCase:
    def __init__(self, repository: AbstractOrganizerRepository) -> None:
        self._repository = repository

    async def execute(
        self, pagination: PaginationParams
    ) -> PaginatedResponse[OrganizerRead]:
        organizers, total = await self._repository.find_all(
            offset=pagination.offset, limit=pagination.size
        )
        return PaginatedResponse.create(
            items=[OrganizerMapper.to_read(o) for o in organizers],
            total=total,
            page=pagination.page,
            size=pagination.size,
        )
