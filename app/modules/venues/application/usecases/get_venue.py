from uuid import UUID

from app.modules.venues.api.dto.responses.venue_responses import VenueReadDetail
from app.modules.venues.application.mappers.venue_mapper import VenueMapper
from app.modules.venues.domain.exceptions.venue_exceptions import VenueNotFoundException
from app.modules.venues.domain.repositories.venue_repository import (
    AbstractVenueRepository,
)


class GetVenueUseCase:
    def __init__(self, repository: AbstractVenueRepository) -> None:
        self._repository = repository

    async def execute(self, public_id: UUID) -> VenueReadDetail:
        venue = await self._repository.find_by_public_id(public_id)
        if not venue:
            raise VenueNotFoundException(str(public_id))
        return VenueMapper.to_detail(venue)