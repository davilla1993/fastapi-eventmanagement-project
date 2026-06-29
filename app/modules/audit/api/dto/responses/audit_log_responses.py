import json
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class AuditLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    entity_type: str
    entity_public_id: uuid.UUID
    action: str
    actor_public_id: uuid.UUID | None = None
    details: dict[str, object] | None = None

    @field_validator("details", mode="before")
    @classmethod
    def parse_details(cls, v: str | None) -> dict[str, object] | None:
        if isinstance(v, str):
            return json.loads(v)
        return v