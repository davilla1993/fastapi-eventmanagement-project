import json
import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.domain.audit_log import AuditLog

logger = logging.getLogger("audit")


class AuditService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def log(
        self,
        entity_type: str,
        entity_public_id: UUID,
        action: str,
        actor_public_id: UUID | None = None,
        details: dict[str, object] | None = None,
    ) -> None:
        record = AuditLog(
            entity_type=entity_type,
            entity_public_id=entity_public_id,
            action=action,
            actor_public_id=actor_public_id,
            details=json.dumps(details, default=str) if details else None,
        )
        self._session.add(record)

        logger.info(
            "audit",
            extra={
                "extra": {
                    "entity_type": entity_type,
                    "entity_public_id": str(entity_public_id),
                    "action": action,
                    "actor": str(actor_public_id) if actor_public_id else None,
                }
            },
        )