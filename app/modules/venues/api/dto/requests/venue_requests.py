from pydantic import BaseModel, Field

from app.shared.types.code_postal_fr import CodePostalFR
from app.shared.types.slug import Slug
from app.shared.types.telephone_e164 import TelephoneE164


class VenueCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255, examples=["Salle Pleyel"])
    slug: Slug = Field(examples=["salle-pleyel"])
    address: str = Field(min_length=5, max_length=500, examples=["252 Rue du Faubourg Saint-Honoré"])  # noqa: E501
    city: str = Field(min_length=1, max_length=100, examples=["Paris"])
    postal_code: CodePostalFR = Field(examples=["75008"])
    capacity: int | None = Field(default=None, ge=1, examples=[1913])
    description: str | None = Field(
        default=None,
        max_length=2000,
        examples=["Salle de concert parisienne inaugurée en 1927."],
    )
    website: str | None = Field(default=None, max_length=500, examples=["https://sallepleyel.fr"])
    telephone: TelephoneE164 | None = Field(default=None, examples=["+33145619650"])


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