from pydantic import BaseModel, Field

from app.shared.types.code_postal_fr import CodePostalFR
from app.shared.types.slug import Slug
from app.shared.types.telephone_e164 import TelephoneE164


class VenueCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    slug: Slug
    address: str = Field(min_length=5, max_length=500)
    city: str = Field(min_length=1, max_length=100)
    postal_code: CodePostalFR
    capacity: int | None = Field(default=None, ge=1)
    description: str | None = Field(default=None, max_length=2000)
    website: str | None = Field(default=None, max_length=500)
    telephone: TelephoneE164 | None = None


class VenueUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    slug: Slug | None = None
    address: str | None = Field(default=None, min_length=5, max_length=500)
    city: str | None = Field(default=None, min_length=1, max_length=100)
    postal_code: CodePostalFR | None = None
    capacity: int | None = Field(default=None, ge=1)
    description: str | None = Field(default=None, max_length=2000)
    website: str | None = Field(default=None, max_length=500)
    telephone: TelephoneE164 | None = None