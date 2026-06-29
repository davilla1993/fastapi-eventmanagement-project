from uuid import UUID

from app.infrastructure.audit.audit_service import AuditService
from app.modules.categories.domain.exceptions.category_exceptions import (
    CategoryNotFoundException,
)
from app.modules.categories.domain.repositories.category_repository import (
    AbstractCategoryRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork


class DeleteCategoryUseCase:
    def __init__(
        self,
        repository: AbstractCategoryRepository,
        uow: UnitOfWork,
        audit: AuditService,
    ) -> None:
        self._repository = repository
        self._uow = uow
        self._audit = audit

    async def execute(self, public_id: UUID, actor_public_id: UUID) -> None:
        category = await self._repository.find_by_public_id(public_id)
        if not category:
            raise CategoryNotFoundException(str(public_id))

        category.deleted_by = actor_public_id
        await self._repository.delete(category)
        await self._audit.log(
            entity_type="category",
            entity_public_id=public_id,
            action="deleted",
            actor_public_id=actor_public_id,
        )
        await self._uow.commit()