import pytest
from pydantic import BaseModel, ValidationError

from app.shared.types.iban import IBAN


class _Model(BaseModel):
    iban: IBAN


# ── Cas valides ───────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "value",
    [
        "FR7630006000011234567890189",  # France
        "DE89370400440532013000",  # Allemagne
        "GB29NWBK60161331926819",  # Royaume-Uni
        "FR76 3000 6000 0112 3456 7890 189",  # avec espaces (normalisé)
    ],
)
def test_iban_valide(value: str) -> None:
    m = _Model(iban=value)
    assert " " not in m.iban  # normalisé sans espaces


# ── Cas invalides ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "value",
    [
        "FR7630006000011234567890188",  # checksum incorrect
        "1234567890",  # pas de code pays
        "FRAB30006000011234567890189",  # chiffres de contrôle non numériques
        "",  # vide
    ],
)
def test_iban_invalide(value: str) -> None:
    with pytest.raises(ValidationError):
        _Model(iban=value)


# ── Normalisation espaces ─────────────────────────────────────────────────────


def test_iban_normalise_espaces() -> None:
    m = _Model(iban="FR76 3000 6000 0112 3456 7890 189")
    assert m.iban == "FR7630006000011234567890189"


# ── Sérialisation ─────────────────────────────────────────────────────────────


def test_iban_serialise_en_str() -> None:
    m = _Model(iban="FR7630006000011234567890189")
    assert m.model_dump()["iban"] == "FR7630006000011234567890189"
    assert isinstance(m.model_dump()["iban"], str)
