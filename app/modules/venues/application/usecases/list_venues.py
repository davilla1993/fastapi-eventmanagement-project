from app.modules.venues.api.dto.responses.venue_responses import VenueRead
from app.modules.venues.application.mappers.venue_mapper import VenueMapper
from app.modules.venues.domain.repositories.venue_repository import (
    AbstractVenueRepository,
)
from app.shared.pagination.schemas import PaginatedResponse, PaginationParams


class ListVenuesUseCase:
    def __init__(self, repository: AbstractVenueRepository) -> None:
        self._repository = repository

    async def execute(
        self, pagination: PaginationParams, city: str | None = None
    ) -> PaginatedResponse[VenueRead]:
        venues, total = await self._repository.find_all(
            offset=pagination.offset, limit=pagination.size, city=city
        )
        return PaginatedResponse.create(
            items=[VenueMapper.to_read(v) for v in venues],
            total=total,
            page=pagination.page,
            size=pagination.size,
        )