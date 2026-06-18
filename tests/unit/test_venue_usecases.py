"""Tests unitaires — use cases Venue (mocks)."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.modules.venues.api.dto.requests.venue_requests import VenueCreate
from app.modules.venues.application.usecases.create_venue import CreateVenueUseCase
from app.modules.venues.application.usecases.get_venue import GetVenueUseCase
from app.modules.venues.domain.entities.venue import Venue
from app.modules.venues.domain.exceptions.venue_exceptions import (
    VenueNotFoundException,
    VenueSlugAlreadyExistsException,
)


def _make_venue(**kwargs: object) -> Venue:
    from datetime import UTC, datetime
    v = Venue(
        name=str(kwargs.get("name", "Salle Test")),
        slug=str(kwargs.get("slug", "salle-test")),
        address="1 Rue de la Paix",
        city="Paris",
        postal_code="75001",
    )
    v.public_id = uuid4()
    v.created_at = datetime.now(UTC)
    v.updated_at = datetime.now(UTC)
    return v


def _venue_create() -> VenueCreate:
    return VenueCreate(
        name="Salle Pleyel",
        slug="salle-pleyel",
        address="252 Rue du Faubourg Saint-Honoré",
        city="Paris",
        postal_code="75008",
        capacity=1913,
    )


@pytest.fixture
def repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def uow() -> AsyncMock:
    return AsyncMock()


async def test_create_venue_succes(repo: AsyncMock, uow: AsyncMock) -> None:
    repo.find_by_slug.return_value = None
    venue = _make_venue()
    repo.save.return_value = venue

    result = await CreateVenueUseCase(repo, uow).execute(_venue_create(), uuid4())

    repo.save.assert_called_once()
    uow.commit.assert_called_once()
    assert result.city == venue.city


async def test_create_venue_slug_existe(repo: AsyncMock, uow: AsyncMock) -> None:
    repo.find_by_slug.return_value = _make_venue()

    with pytest.raises(VenueSlugAlreadyExistsException):
        await CreateVenueUseCase(repo, uow).execute(_venue_create(), uuid4())

    repo.save.assert_not_called()


async def test_get_venue_introuvable(repo: AsyncMock) -> None:
    repo.find_by_public_id.return_value = None

    with pytest.raises(VenueNotFoundException):
        await GetVenueUseCase(repo).execute(uuid4())


async def test_get_venue_succes(repo: AsyncMock) -> None:
    venue = _make_venue()
    repo.find_by_public_id.return_value = venue

    result = await GetVenueUseCase(repo).execute(venue.public_id)
    assert result.slug == venue.slug