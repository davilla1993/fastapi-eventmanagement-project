import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.domain.base import Base


class AuditLog(Base):
    """Table append-only — jamais modifiée ni supprimée."""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entity_public_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), nullable=False, index=True
    )
    action: Mapped[str] = mapped_column(String(20), nullable=False)
    actor_public_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), nullable=True
    )
    details: Mapped[str | None] = mapped_column(Text, nullable=True)