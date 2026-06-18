from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.security.dependencies import (
    CurrentUser,
    get_current_user,
    require_organizer,
)
from app.modules.venues.api.dto.requests.venue_requests import VenueCreate, VenueUpdate
from app.modules.venues.api.dto.responses.venue_responses import (
    VenueRead,
    VenueReadDetail,
)
from app.modules.venues.application.usecases.create_venue import CreateVenueUseCase
from app.modules.venues.application.usecases.delete_venue import DeleteVenueUseCase
from app.modules.venues.application.usecases.get_venue import GetVenueUseCase
from app.modules.venues.application.usecases.list_venues import ListVenuesUseCase
from app.modules.venues.application.usecases.update_venue import UpdateVenueUseCase
from app.modules.venues.infrastructure.repositories.sqlalchemy_venue_repository import (  # noqa: E501
    SqlAlchemyVenueRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork
from app.shared.pagination.schemas import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/venues", tags=["Venues"])


@router.post(
    "",
    response_model=VenueReadDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une salle",
    description="Crée une nouvelle salle ou lieu d'accueil. Réservé aux rôles ORGANIZER et ADMIN.",
    response_description="Salle créée avec succès.",
)
async def create_venue(
    body: VenueCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(require_organizer),
) -> VenueReadDetail:
    repo = SqlAlchemyVenueRepository(db)
    uow = UnitOfWork(db)
    return await CreateVenueUseCase(repo, uow).execute(body, current_user.public_id)


@router.get(
    "",
    response_model=PaginatedResponse[VenueRead],
    summary="Lister les salles",
    description="Retourne la liste paginée des salles. Filtrable par ville (recherche partielle insensible à la casse).",  # noqa: E501
    response_description="Liste paginée de salles.",
)
async def list_venues(
    pagination: PaginationParams = Depends(),
    city: str | None = Query(default=None, description="Filtrer par ville (recherche partielle)"),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[VenueRead]:
    repo = SqlAlchemyVenueRepository(db)
    return await ListVenuesUseCase(repo).execute(pagination, city=city)


@router.get(
    "/{public_id}",
    response_model=VenueReadDetail,
    summary="Obtenir une salle",
    description="Retourne le détail complet d'une salle par son identifiant public (UUID).",
    response_description="Détail de la salle.",
)
async def get_venue(
    public_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> VenueReadDetail:
    repo = SqlAlchemyVenueRepository(db)
    return await GetVenueUseCase(repo).execute(public_id)


@router.patch(
    "/{public_id}",
    response_model=VenueReadDetail,
    summary="Mettre à jour une salle",
    description="Met à jour les informations d'une salle existante. Réservé aux rôles ORGANIZER et ADMIN.",  # noqa: E501
    response_description="Salle mise à jour.",
)
async def update_venue(
    public_id: UUID,
    body: VenueUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(require_organizer),
) -> VenueReadDetail:
    repo = SqlAlchemyVenueRepository(db)
    uow = UnitOfWork(db)
    return await UpdateVenueUseCase(repo, uow).execute(
        public_id, body, current_user.public_id
    )


@router.delete(
    "/{public_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer une salle",
    description="Suppression logique (soft delete) d'une salle. Nécessite d'être authentifié.",
    response_description="Suppression effectuée (aucun contenu retourné).",
)
async def delete_venue(
    public_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> None:
    repo = SqlAlchemyVenueRepository(db)
    uow = UnitOfWork(db)
    await DeleteVenueUseCase(repo, uow).execute(public_id, current_user.public_id)