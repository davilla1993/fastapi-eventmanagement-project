import re
from typing import Annotated

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

_CODE_POSTAL_RE = re.compile(r"^(?:0[1-9]|[1-8]\d|9[0-5])\d{3}$")


class CodePostalFR(str):
    """Code postal français : 5 chiffres, départements 01–95 (hors DOM-TOM)."""

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
    def _validate(cls, value: str) -> "CodePostalFR":
        if not _CODE_POSTAL_RE.match(value):
            raise ValueError(
                f"Code postal invalide : '{value}'. "
                "Format attendu : 5 chiffres, département 01–95 (ex: 75001)."
            )
        return cls(value)


CodePostalFRType = Annotated[CodePostalFR, ...]
