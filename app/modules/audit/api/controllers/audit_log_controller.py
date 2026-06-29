from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.audit.audit_service import AuditService
from app.infrastructure.database.session import get_db
from app.infrastructure.security.dependencies import require_admin
from app.modules.audit.api.dto.responses.audit_log_responses import AuditLogRead
from app.shared.pagination.schemas import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@router.get(
    "",
    response_model=PaginatedResponse[AuditLogRead],
    summary="Consulter les logs d'audit",
    description=(
        "Retourne la liste paginée des entrées d'audit, triées par date décroissante. "
        "Filtrable par type d'entité (`event`, `venue`, `organizer`, `category`), "
        "identifiant, action (`created`, `updated`, `deleted`) et acteur. "
        "**Réservé aux ADMINs.**"
    ),
    response_description="Liste paginée des entrées d'audit.",
)
async def list_audit_logs(
    pagination: PaginationParams = Depends(),
    entity_type: str | None = Query(default=None, description="event | venue | organizer | category"),
    entity_public_id: UUID | None = Query(default=None),
    action: str | None = Query(default=None, description="created | updated | deleted"),
    actor_public_id: UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
    _: object = Depends(require_admin),
) -> PaginatedResponse[AuditLogRead]:
    audit = AuditService(db)
    items, total = await audit.list(
        entity_type=entity_type,
        entity_public_id=entity_public_id,
        action=action,
        actor_public_id=actor_public_id,
        offset=pagination.offset,
        limit=pagination.size,
    )
    return PaginatedResponse.create(
        items=[AuditLogRead.model_validate(item) for item in items],
        total=total,
        page=pagination.page,
        size=pagination.size,
    )