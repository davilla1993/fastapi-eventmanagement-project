import re
from typing import Annotated

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

_IBAN_RE = re.compile(r"^[A-Z]{2}\d{2}[A-Z0-9]{4,30}$")


class IBAN(str):
    """IBAN international avec vérification du checksum MOD-97."""

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
    def _validate(cls, value: str) -> "IBAN":
        normalized = value.replace(" ", "").upper()

        if not _IBAN_RE.match(normalized):
            raise ValueError(
                f"IBAN invalide : '{value}'. "
                "Format attendu : 2 lettres pays + 2 chiffres de contrôle + BBAN "
                "(ex: FR7630006000011234567890189)."
            )

        if not cls._check_mod97(normalized):
            raise ValueError(f"IBAN invalide : '{value}'. Checksum MOD-97 incorrect.")

        return cls(normalized)

    @staticmethod
    def _check_mod97(iban: str) -> bool:
        rearranged = iban[4:] + iban[:4]
        numeric = "".join(
            str(ord(c) - ord("A") + 10) if c.isalpha() else c for c in rearranged
        )
        return int(numeric) % 97 == 1


IBANType = Annotated[IBAN, ...]
