"""Tests property-based avec Hypothesis pour les 5 types personnalisés."""

import re
import string

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from app.shared.types.code_postal_fr import CodePostalFR
from app.shared.types.iban import IBAN
from app.shared.types.slug import Slug
from app.shared.types.telephone_e164 import TelephoneE164
from app.shared.types.url_image import URLImage

# ── Stratégies valides ────────────────────────────────────────────────────────

slug_strategy = st.from_regex(r"[a-z0-9]+(?:-[a-z0-9]+)*", fullmatch=True)

url_image_strategy = st.builds(
    lambda domain, name, ext: f"https://{domain}/{name}.{ext}",
    domain=st.from_regex(r"[a-z]{3,10}\.[a-z]{2,4}", fullmatch=True),
    name=st.from_regex(r"[a-z0-9_-]{3,20}", fullmatch=True),
    ext=st.sampled_from(["jpg", "jpeg", "png", "webp"]),
)

code_postal_strategy = st.builds(
    lambda dept, suffix: f"{dept:02d}{suffix:03d}",
    dept=st.integers(min_value=1, max_value=95),
    suffix=st.integers(min_value=0, max_value=999),
)

telephone_strategy = st.builds(
    lambda cc, number: f"+{cc}{number}",
    cc=st.integers(min_value=1, max_value=99),
    number=st.from_regex(r"[1-9]\d{5,11}", fullmatch=True),
)


def _make_valid_iban_fr() -> st.SearchStrategy[str]:
    """Génère un IBAN FR valide avec checksum correct."""

    def build(bban: str) -> str:
        raw = bban + "FR00"
        numeric = "".join(
            str(ord(c) - ord("A") + 10) if c.isalpha() else c for c in raw
        )
        check = 98 - (int(numeric) % 97)
        return f"FR{check:02d}{bban}"

    return st.from_regex(r"[0-9]{23}", fullmatch=True).map(build)


# ── Slug ──────────────────────────────────────────────────────────────────────


@given(slug_strategy)
@settings(max_examples=200)
def test_slug_valide_accepte(value: str) -> None:
    assert Slug._validate(value) == value


@given(
    st.text(min_size=1).filter(lambda s: not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", s))
)
@settings(max_examples=100)
def test_slug_invalide_rejete(value: str) -> None:
    with pytest.raises(ValueError):
        Slug._validate(value)


# ── URLImage ──────────────────────────────────────────────────────────────────


@given(url_image_strategy)
@settings(max_examples=200)
def test_url_image_valide_accepte(url: str) -> None:
    result = URLImage._validate(url)
    assert result.startswith("https://")


@given(
    st.text(alphabet=string.ascii_letters + string.digits + "/:.-_", min_size=5).filter(
        lambda s: not s.startswith("https://")
    )
)
@settings(max_examples=100)
def test_url_image_non_https_rejete(url: str) -> None:
    with pytest.raises(ValueError):
        URLImage._validate(url)


# ── CodePostalFR ──────────────────────────────────────────────────────────────


@given(code_postal_strategy)
@settings(max_examples=200)
def test_code_postal_valide_accepte(code: str) -> None:
    assert len(CodePostalFR._validate(code)) == 5


@given(
    st.text(alphabet=string.digits, min_size=5, max_size=5).filter(
        lambda s: not re.match(r"^(?:0[1-9]|[1-8]\d|9[0-5])\d{3}$", s)
    )
)
@settings(max_examples=100)
def test_code_postal_invalide_rejete(code: str) -> None:
    with pytest.raises(ValueError):
        CodePostalFR._validate(code)


# ── TelephoneE164 ─────────────────────────────────────────────────────────────


@given(telephone_strategy)
@settings(max_examples=200)
def test_telephone_valide_accepte(tel: str) -> None:
    result = TelephoneE164._validate(tel)
    assert result.startswith("+")


@given(
    st.text(alphabet=string.digits, min_size=7, max_size=15).filter(
        lambda s: not s.startswith("+")
    )
)
@settings(max_examples=100)
def test_telephone_sans_plus_rejete(tel: str) -> None:
    with pytest.raises(ValueError):
        TelephoneE164._validate(tel)


# ── IBAN ──────────────────────────────────────────────────────────────────────


@given(_make_valid_iban_fr())
@settings(max_examples=100)
def test_iban_valide_accepte(iban: str) -> None:
    result = IBAN._validate(iban)
    assert result.startswith("FR")


@given(
    st.from_regex(r"[A-Z]{2}[0-9]{2}[A-Z0-9]{6,30}", fullmatch=True).filter(
        lambda s: not (len(s) >= 4 and s[2:4].isdigit() and IBAN._check_mod97(s))
    )
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
def test_iban_checksum_invalide_rejete(value: str) -> None:
    with pytest.raises(ValueError):
        IBAN._validate(value)
