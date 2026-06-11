import re
from typing import Annotated
from urllib.parse import urlparse

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

_ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
_ALLOWED_DOMAINS_RE = re.compile(r".+")  # tout domaine autorisé par défaut


class URLImage(str):
    """URL d'image HTTPS avec extension autorisée (jpg, jpeg, png, webp)."""

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
    def _validate(cls, value: str) -> "URLImage":
        parsed = urlparse(value)

        if parsed.scheme != "https":
            raise ValueError(
                f"URLImage invalide : schéma HTTPS requis (reçu '{parsed.scheme}')."
            )

        if not parsed.netloc:
            raise ValueError("URLImage invalide : domaine manquant.")

        path = parsed.path.lower()
        extension = path.rsplit(".", 1)[-1] if "." in path else ""
        if extension not in _ALLOWED_EXTENSIONS:
            raise ValueError(
                f"URLImage invalide : extension '{extension}' non autorisée. "
                f"Extensions acceptées : {sorted(_ALLOWED_EXTENSIONS)}."
            )

        return cls(value)


URLImageType = Annotated[URLImage, ...]
