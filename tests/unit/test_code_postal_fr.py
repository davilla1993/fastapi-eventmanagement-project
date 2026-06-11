import pytest
from pydantic import BaseModel, ValidationError

from app.shared.types.code_postal_fr import CodePostalFR


class _Model(BaseModel):
    code: CodePostalFR


# ── Cas valides ───────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "value",
    [
        "75001",  # Paris 1er
        "01000",  # Ain
        "95999",  # Val-d'Oise
        "33000",  # Bordeaux
        "69001",  # Lyon
        "13001",  # Marseille
    ],
)
def test_code_postal_valide(value: str) -> None:
    assert _Model(code=value).code == value


# ── Cas invalides ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "value",
    [
        "00000",  # département 00 inexistant
        "96000",  # DOM-TOM hors périmètre
        "99000",  # inexistant
        "7500",  # trop court
        "750011",  # trop long
        "7500A",  # lettre
        "",  # vide
    ],
)
def test_code_postal_invalide(value: str) -> None:
    with pytest.raises(ValidationError):
        _Model(code=value)


# ── Sérialisation ─────────────────────────────────────────────────────────────


def test_code_postal_serialise_en_str() -> None:
    m = _Model(code="75001")
    assert m.model_dump()["code"] == "75001"
    assert isinstance(m.model_dump()["code"], str)
