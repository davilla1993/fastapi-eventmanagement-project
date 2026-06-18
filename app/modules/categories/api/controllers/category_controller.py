from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.security.dependencies import (
    CurrentUser,
    get_current_user,
    require_admin,
)
from app.modules.categories.api.dto.requests.category_requests import (
    CategoryCreate,
    CategoryUpdate,
)
from app.modules.categories.api.dto.responses.category_responses import (
    CategoryRead,
    CategoryReadDetail,
)
from app.modules.categories.application.usecases.create_category import (
    CreateCategoryUseCase,
)
from app.modules.categories.application.usecases.delete_category import (
    DeleteCategoryUseCase,
)
from app.modules.categories.application.usecases.get_category import GetCategoryUseCase
from app.modules.categories.application.usecases.list_categories import (
    ListCategoriesUseCase,
)
from app.modules.categories.application.usecases.update_category import (
    UpdateCategoryUseCase,
)
from app.modules.categories.infrastructure.repositories.sqlalchemy_category_repository import (  # noqa: E501
    SqlAlchemyCategoryRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork
from app.shared.pagination.schemas import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post(
    "",
    response_model=CategoryReadDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une catégorie",
    description="Crée une nouvelle catégorie thématique. **Réservé aux ADMINs.**",
    response_description="Catégorie créée avec succès.",
)
async def create_category(
    body: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(require_admin),
) -> CategoryReadDetail:
    repo = SqlAlchemyCategoryRepository(db)
    uow = UnitOfWork(db)
    return await CreateCategoryUseCase(repo, uow).execute(body, current_user.public_id)


@router.get(
    "",
    response_model=PaginatedResponse[CategoryRead],
    summary="Lister les catégories",
    description="Retourne la liste paginée des catégories. Accessible publiquement.",
    response_description="Liste paginée de catégories.",
)
async def list_categories(
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[CategoryRead]:
    repo = SqlAlchemyCategoryRepository(db)
    return await ListCategoriesUseCase(repo).execute(pagination)


@router.get(
    "/{public_id}",
    response_model=CategoryReadDetail,
    summary="Obtenir une catégorie",
    description="Retourne le détail d'une catégorie par son identifiant public (UUID).",
    response_description="Détail de la catégorie.",
)
async def get_category(
    public_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> CategoryReadDetail:
    repo = SqlAlchemyCategoryRepository(db)
    return await GetCategoryUseCase(repo).execute(public_id)


@router.patch(
    "/{public_id}",
    response_model=CategoryReadDetail,
    summary="Mettre à jour une catégorie",
    description="Met à jour une catégorie existante. **Réservé aux ADMINs.**",
    response_description="Catégorie mise à jour.",
)
async def update_category(
    public_id: UUID,
    body: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(require_admin),
) -> CategoryReadDetail:
    repo = SqlAlchemyCategoryRepository(db)
    uow = UnitOfWork(db)
    return await UpdateCategoryUseCase(repo, uow).execute(
        public_id, body, current_user.public_id
    )


@router.delete(
    "/{public_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer une catégorie",
    description="Suppression logique (soft delete) d'une catégorie. Nécessite d'être authentifié.",
    response_description="Suppression effectuée (aucun contenu retourné).",
)
async def delete_category(
    public_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> None:
    repo = SqlAlchemyCategoryRepository(db)
    uow = UnitOfWork(db)
    await DeleteCategoryUseCase(repo, uow).execute(public_id, current_user.public_id)