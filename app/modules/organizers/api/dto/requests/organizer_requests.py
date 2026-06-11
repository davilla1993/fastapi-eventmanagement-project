from pydantic import BaseModel, EmailStr, Field

from app.shared.types.telephone_e164 import TelephoneE164


class OrganizerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    telephone: TelephoneE164 | None = None
    website: str | None = Field(default=None, max_length=500)
    description: str | None = Field(default=None, max_length=2000)


class OrganizerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    email: EmailStr | None = None
    telephone: TelephoneE164 | None = None
    website: str | None = Field(default=None, max_length=500)
    description: str | None = Field(default=None, max_length=2000)
