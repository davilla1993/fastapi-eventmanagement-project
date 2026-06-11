import re
from typing import Annotated

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class Slug(str):
    """Identifiant URL-safe : minuscules, chiffres, tirets. Ex: mon-evenement-2024"""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: object, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def _validate(cls, value: str) -> "Slug":
        if not _SLUG_RE.match(value):
            raise ValueError(
                f"Slug invalide : '{value}'. "
                "Format attendu : minuscules, chiffres et tirets uniquement "
                "(ex: mon-evenement-2024)."
            )
        return cls(value)

    @classmethod
    def from_title(cls, title: str) -> "Slug":
        import unicodedata

        normalized = unicodedata.normalize("NFD", title.lower())
        ascii_str = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
        slug = re.sub(r"[^a-z0-9]+", "-", ascii_str).strip("-")
        return cls._validate(slug)


SlugType = Annotated[Slug, ...]
