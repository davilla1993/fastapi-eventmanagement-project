from uuid import UUID

from app.infrastructure.audit.audit_service import AuditService
from app.modules.venues.api.dto.requests.venue_requests import VenueUpdate
from app.modules.venues.api.dto.responses.venue_responses import VenueReadDetail
from app.modules.venues.application.mappers.venue_mapper import VenueMapper
from app.modules.venues.domain.exceptions.venue_exceptions import (
    VenueNotFoundException,
    VenueSlugAlreadyExistsException,
)
from app.modules.venues.domain.repositories.venue_repository import (
    AbstractVenueRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork


class UpdateVenueUseCase:
    def __init__(
        self, repository: AbstractVenueRepository, uow: UnitOfWork, audit: AuditService
    ) -> None:
        self._repository = repository
        self._uow = uow
        self._audit = audit

    async def execute(
        self, public_id: UUID, request: VenueUpdate, actor_public_id: UUID
    ) -> VenueReadDetail:
        venue = await self._repository.find_by_public_id(public_id)
        if not venue:
            raise VenueNotFoundException(str(public_id))

        if request.slug is not None and str(request.slug) != venue.slug:
            if await self._repository.find_by_slug(str(request.slug)):
                raise VenueSlugAlreadyExistsException(str(request.slug))
            venue.slug = str(request.slug)

        if request.name is not None:
            venue.name = request.name
        if request.address is not None:
            venue.address = request.address
        if request.city is not None:
            venue.city = request.city
        if request.postal_code is not None:
            venue.postal_code = str(request.postal_code)
        if request.capacity is not None:
            venue.capacity = request.capacity
        if request.description is not None:
            venue.description = request.description
        if request.website is not None:
            venue.website = request.website
        if request.telephone is not None:
            venue.telephone = str(request.telephone)

        venue.updated_by = actor_public_id
        saved = await self._repository.save(venue)
        await self._audit.log(
            entity_type="venue",
            entity_public_id=saved.public_id,
            action="updated",
            actor_public_id=actor_public_id,
            details={"name": saved.name, "city": saved.city},
        )
        await self._uow.commit()
        return VenueMapper.to_detail(saved)