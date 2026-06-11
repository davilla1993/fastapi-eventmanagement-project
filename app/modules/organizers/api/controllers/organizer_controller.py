from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.security.dependencies import (
    CurrentUser,
    get_current_user,
    require_organizer,
)
from app.modules.organizers.api.dto.requests.organizer_requests import (
    OrganizerCreate,
    OrganizerUpdate,
)
from app.modules.organizers.api.dto.responses.organizer_responses import (
    OrganizerRead,
    OrganizerReadDetail,
)
from app.modules.organizers.application.usecases.create_organizer import (
    CreateOrganizerUseCase,
)
from app.modules.organizers.application.usecases.delete_organizer import (
    DeleteOrganizerUseCase,
)
from app.modules.organizers.application.usecases.get_organizer import (
    GetOrganizerUseCase,
)
from app.modules.organizers.application.usecases.list_organizers import (
    ListOrganizersUseCase,
)
from app.modules.organizers.application.usecases.update_organizer import (
    UpdateOrganizerUseCase,
)
from app.modules.organizers.infrastructure.repositories.sqlalchemy_organizer_repository import (  # noqa: E501
    SqlAlchemyOrganizerRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork
from app.shared.pagination.schemas import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/organizers", tags=["Organizers"])


@router.post(
    "", response_model=OrganizerReadDetail, status_code=status.HTTP_201_CREATED
)
async def create_organizer(
    body: OrganizerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(require_organizer),
) -> OrganizerReadDetail:
    repo = SqlAlchemyOrganizerRepository(db)
    uow = UnitOfWork(db)
    return await CreateOrganizerUseCase(repo, uow).execute(body, current_user.public_id)


@router.get("", response_model=PaginatedResponse[OrganizerRead])
async def list_organizers(
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[OrganizerRead]:
    repo = SqlAlchemyOrganizerRepository(db)
    return await ListOrganizersUseCase(repo).execute(pagination)


@router.get("/{public_id}", response_model=OrganizerReadDetail)
async def get_organizer(
    public_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> OrganizerReadDetail:
    repo = SqlAlchemyOrganizerRepository(db)
    return await GetOrganizerUseCase(repo).execute(public_id)


@router.patch("/{public_id}", response_model=OrganizerReadDetail)
async def update_organizer(
    public_id: UUID,
    body: OrganizerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> OrganizerReadDetail:
    repo = SqlAlchemyOrganizerRepository(db)
    uow = UnitOfWork(db)
    return await UpdateOrganizerUseCase(repo, uow).execute(
        public_id, body, current_user.public_id, current_user.role
    )


@router.delete("/{public_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organizer(
    public_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> None:
    repo = SqlAlchemyOrganizerRepository(db)
    uow = UnitOfWork(db)
    await DeleteOrganizerUseCase(repo, uow).execute(public_id, current_user.public_id)
