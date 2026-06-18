import re

from pydantic import BaseModel, Field, field_validator

from app.shared.types.slug import Slug


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255, examples=["Jazz"])
    slug: Slug = Field(examples=["jazz"])
    description: str | None = Field(
        default=None,
        max_length=2000,
        examples=["Concerts et événements autour du jazz et de ses dérivés."],
    )
    color: str | None = Field(  # noqa: E501
        default=None, description="Couleur hexadécimale (#RRGGBB)", examples=["#F59E0B"]
    )

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str | None) -> str | None:
        if v is not None and not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("La couleur doit être au format hexadécimal (#RRGGBB)")
        return v


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    slug: Slug | None = None
    description: str | None = Field(default=None, max_length=2000)
    color: str | None = Field(  # noqa: E501
        default=None, description="Couleur hexadécimale (#RRGGBB)", examples=["#F59E0B"]
    )

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str | None) -> str | None:
        if v is not None and not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("La couleur doit être au format hexadécimal (#RRGGBB)")
        return v