from uuid import UUID

from app.infrastructure.audit.audit_service import AuditService
from app.modules.venues.api.dto.requests.venue_requests import VenueCreate
from app.modules.venues.api.dto.responses.venue_responses import VenueReadDetail
from app.modules.venues.application.mappers.venue_mapper import VenueMapper
from app.modules.venues.domain.entities.venue import Venue
from app.modules.venues.domain.exceptions.venue_exceptions import (
    VenueSlugAlreadyExistsException,
)
from app.modules.venues.domain.repositories.venue_repository import (
    AbstractVenueRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork


class CreateVenueUseCase:
    def __init__(
        self, repository: AbstractVenueRepository, uow: UnitOfWork, audit: AuditService
    ) -> None:
        self._repository = repository
        self._uow = uow
        self._audit = audit

    async def execute(
        self, request: VenueCreate, actor_public_id: UUID
    ) -> VenueReadDetail:
        if await self._repository.find_by_slug(str(request.slug)):
            raise VenueSlugAlreadyExistsException(str(request.slug))

        venue = Venue(
            name=request.name,
            slug=str(request.slug),
            address=request.address,
            city=request.city,
            postal_code=str(request.postal_code),
            capacity=request.capacity,
            description=request.description,
            website=request.website,
            telephone=str(request.telephone) if request.telephone else None,
            created_by=actor_public_id,
            updated_by=actor_public_id,
        )
        saved = await self._repository.save(venue)
        await self._audit.log(
            entity_type="venue",
            entity_public_id=saved.public_id,
            action="created",
            actor_public_id=actor_public_id,
            details={"name": saved.name, "city": saved.city},
        )
        await self._uow.commit()
        return VenueMapper.to_detail(saved)