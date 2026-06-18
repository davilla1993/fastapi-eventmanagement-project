from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator

from app.shared.types.slug import Slug
from app.shared.types.url_image import URLImage


class _EventBase(BaseModel):
    title: str = Field(min_length=2, max_length=255, examples=["Jazz Festival Paris 2025"])  # noqa: E501
    slug: Slug = Field(examples=["jazz-festival-paris-2025"])
    description: str | None = Field(
        default=None,
        max_length=5000,
        examples=["Le plus grand festival de jazz de la capitale."],
    )
    status: Literal["draft", "published", "cancelled", "sold_out"] = Field(
        default="draft", examples=["published"]
    )
    start_at: datetime = Field(examples=["2025-07-14T20:00:00+02:00"])
    end_at: datetime = Field(examples=["2025-07-14T23:30:00+02:00"])
    venue_public_id: UUID = Field(examples=["550e8400-e29b-41d4-a716-446655440000"])
    organizer_public_id: UUID = Field(examples=["550e8400-e29b-41d4-a716-446655440001"])
    category_public_id: UUID | None = Field(
        default=None, examples=["550e8400-e29b-41d4-a716-446655440002"]
    )
    city: str = Field(min_length=1, max_length=100, examples=["Paris"])
    price: Decimal | None = Field(default=None, ge=0, examples=["45.00"])
    capacity: int | None = Field(default=None, ge=1, examples=[500])
    image_url: URLImage | None = Field(
        default=None, examples=["https://example.com/jazz-festival.jpg"]
    )
    tags: str | None = Field(
        default=None,
        max_length=500,
        description="Tags séparés par des virgules",
        examples=["jazz,bebop,improvisation"],
    )

    @model_validator(mode="after")
    def check_dates(self) -> "_EventBase":
        if self.end_at <= self.start_at:
            raise ValueError("La date de fin doit être postérieure à la date de début.")
        return self


class ConcertCreate(_EventBase):
    event_type: Literal["concert"] = "concert"
    artist: str = Field(min_length=1, max_length=255, examples=["Ibrahim Maalouf"])
    genre: str | None = Field(default=None, max_length=100, examples=["Jazz contemporain"])  # noqa: E501


class TheatreCreate(_EventBase):
    event_type: Literal["theatre"] = "theatre"
    director: str | None = Field(default=None, max_length=255, examples=["Ariane Mnouchkine"])  # noqa: E501
    cast_members: str | None = Field(
        default=None, max_length=2000, examples=["Sophie Marceau, Vincent Cassel"]
    )


class ConferenceCreate(_EventBase):
    event_type: Literal["conference"] = "conference"
    speaker: str = Field(min_length=1, max_length=255, examples=["Pr. Jean Dupont"])
    topic: str | None = Field(
        default=None, max_length=255, examples=["Intelligence Artificielle et Créativité"]  # noqa: E501
    )


EventCreate = Annotated[
    ConcertCreate | TheatreCreate | ConferenceCreate,
    Field(discriminator="event_type"),
]


class EventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    slug: Slug | None = None
    description: str | None = Field(default=None, max_length=5000)
    status: Literal["draft", "published", "cancelled", "sold_out"] | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    city: str | None = Field(default=None, min_length=1, max_length=100)
    price: Decimal | None = Field(default=None, ge=0)
    capacity: int | None = Field(default=None, ge=1)
    image_url: URLImage | None = None
    tags: str | None = Field(default=None, max_length=500)
    artist: str | None = Field(default=None, max_length=255)
    genre: str | None = Field(default=None, max_length=100)
    director: str | None = Field(default=None, max_length=255)
    cast_members: str | None = Field(default=None, max_length=2000)
    speaker: str | None = Field(default=None, max_length=255)
    topic: str | None = Field(default=None, max_length=255)

    @field_validator("start_at", "end_at", mode="before")
    @classmethod
    def allow_none(cls, v: object) -> object:
        return v