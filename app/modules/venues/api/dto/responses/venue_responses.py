import uuid
from datetime import datetime

from pydantic import BaseModel


class VenueRead(BaseModel):
    public_id: uuid.UUID
    name: str
    slug: str
    city: str
    postal_code: str
    capacity: int | None

    model_config = {"from_attributes": True}


class VenueReadDetail(BaseModel):
    public_id: uuid.UUID
    name: str
    slug: str
    address: str
    city: str
    postal_code: str
    capacity: int | None
    description: str | None
    website: str | None
    telephone: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}