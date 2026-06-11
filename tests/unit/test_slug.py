import pytest
from pydantic import BaseModel, ValidationError

from app.shared.types.slug import Slug


class _Model(BaseModel):
    slug: Slug


# ── Cas valides ───────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "value",
    [
        "mon-evenement",
        "concert2024",
        "a",
        "abc-123-def",
        "jazz-festival-paris-2024",
    ],
)
def test_slug_valide(value: str) -> None:
    assert _Model(slug=value).slug == value


# ── Cas invalides ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "value",
    [
        "Mon-Evenement",  # majuscules
        "mon evenement",  # espace
        "mon_evenement",  # underscore
        "-leading-dash",  # tiret en début
        "trailing-dash-",  # tiret en fin
        "double--dash",  # double tiret
        "événement",  # accent
        "",  # vide
    ],
)
def test_slug_invalide(value: str) -> None:
    with pytest.raises(ValidationError):
        _Model(slug=value)


# ── from_title ────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "title, expected",
    [
        ("Mon Événement 2024", "mon-evenement-2024"),
        ("Jazz & Blues Festival", "jazz-blues-festival"),
        ("Conférence IA", "conference-ia"),
        ("  Spaces  ", "spaces"),
    ],
)
def test_slug_from_title(title: str, expected: str) -> None:
    assert Slug.from_title(title) == expected


# ── Sérialisation ─────────────────────────────────────────────────────────────


def test_slug_serialise_en_str() -> None:
    m = _Model(slug="mon-slug")
    assert m.model_dump()["slug"] == "mon-slug"
    assert isinstance(m.model_dump()["slug"], str)
