import pytest
from pydantic import BaseModel, ValidationError

from app.shared.types.url_image import URLImage


class _Model(BaseModel):
    image: URLImage


# ── Cas valides ───────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "url",
    [
        "https://cdn.example.com/photo.jpg",
        "https://images.site.fr/banner.jpeg",
        "https://storage.io/img/cover.png",
        "https://assets.cdn.net/hero.webp",
        "https://example.com/path/to/image.JPG",  # casse extension
    ],
)
def test_url_image_valide(url: str) -> None:
    assert _Model(image=url).image == url


# ── Cas invalides ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "url",
    [
        "http://cdn.example.com/photo.jpg",  # HTTP non HTTPS
        "ftp://cdn.example.com/photo.png",  # mauvais schéma
        "https://cdn.example.com/photo.gif",  # extension non autorisée
        "https://cdn.example.com/photo.bmp",  # extension non autorisée
        "https://cdn.example.com/photo",  # pas d'extension
        "not-a-url",  # pas une URL
        "",  # vide
    ],
)
def test_url_image_invalide(url: str) -> None:
    with pytest.raises(ValidationError):
        _Model(image=url)


# ── Sérialisation ─────────────────────────────────────────────────────────────


def test_url_image_serialise_en_str() -> None:
    url = "https://cdn.example.com/photo.png"
    m = _Model(image=url)
    assert m.model_dump()["image"] == url
    assert isinstance(m.model_dump()["image"], str)
