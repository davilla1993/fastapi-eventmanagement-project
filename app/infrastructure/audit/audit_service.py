import json
import logging
from uuid import UUID

from sqlalchemy import func, select
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

    async def list(
        self,
        entity_type: str | None = None,
        entity_public_id: UUID | None = None,
        action: str | None = None,
        actor_public_id: UUID | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[AuditLog], int]:
        filters = []
        if entity_type:
            filters.append(AuditLog.entity_type == entity_type)
        if entity_public_id:
            filters.append(AuditLog.entity_public_id == entity_public_id)
        if action:
            filters.append(AuditLog.action == action)
        if actor_public_id:
            filters.append(AuditLog.actor_public_id == actor_public_id)

        count_q = select(func.count()).select_from(AuditLog)
        data_q = select(AuditLog).order_by(AuditLog.created_at.desc())
        for f in filters:
            count_q = count_q.where(f)
            data_q = data_q.where(f)

        total = (await self._session.execute(count_q)).scalar_one()
        rows = (
            await self._session.execute(data_q.offset(offset).limit(limit))
        ).scalars().all()
        return list(rows), total