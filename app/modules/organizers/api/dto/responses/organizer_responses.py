import uuid
from datetime import datetime

from pydantic import BaseModel


class OrganizerRead(BaseModel):
    public_id: uuid.UUID
    name: str
    email: str
    telephone: str | None
    website: str | None

    model_config = {"from_attributes": True}


class OrganizerReadDetail(BaseModel):
    public_id: uuid.UUID
    name: str
    email: str
    telephone: str | None
    website: str | None
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
