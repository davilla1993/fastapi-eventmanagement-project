"""Tests unitaires — use cases Event (mocks)."""

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.modules.events.api.dto.requests.event_requests import (
    ConcertCreate,
)
from app.modules.events.application.usecases.create_event import CreateEventUseCase
from app.modules.events.application.usecases.delete_event import DeleteEventUseCase
from app.modules.events.application.usecases.get_event import GetEventUseCase
from app.modules.events.domain.entities.event import Event, EventStatus, EventType
from app.modules.events.domain.exceptions.event_exceptions import (
    EventNotFoundException,
    EventSlugAlreadyExistsException,
)


def _make_event(**kwargs: object) -> Event:
    now = datetime.now(UTC)
    e = Event(
        title=str(kwargs.get("title", "Test Concert")),
        slug=str(kwargs.get("slug", "test-concert")),
        event_type=str(kwargs.get("event_type", EventType.CONCERT)),
        status=str(kwargs.get("status", EventStatus.DRAFT)),
        start_at=kwargs.get("start_at", now + timedelta(days=10)),  # type: ignore[arg-type]
        end_at=kwargs.get("end_at", now + timedelta(days=10, hours=3)),  # type: ignore[arg-type]
        venue_public_id=uuid4(),
        organizer_public_id=uuid4(),
        city="Paris",
        artist="Test Artist",
    )
    e.public_id = uuid4()
    e.created_at = now
    e.updated_at = now
    return e


def _concert_create() -> ConcertCreate:
    now = datetime.now(UTC)
    return ConcertCreate(
        title="Jazz Festival",
        slug="jazz-festival",
        event_type="concert",
        start_at=now + timedelta(days=10),
        end_at=now + timedelta(days=10, hours=3),
        venue_public_id=uuid4(),
        organizer_public_id=uuid4(),
        city="Paris",
        artist="Ibrahim Maalouf",
    )


@pytest.fixture
def repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def uow() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def audit() -> AsyncMock:
    return AsyncMock()


# ── CreateEventUseCase ────────────────────────────────────────────────────────


async def test_create_event_succes(
    repo: AsyncMock, uow: AsyncMock, audit: AsyncMock
) -> None:
    repo.find_by_slug.return_value = None
    event = _make_event()
    repo.save.return_value = event

    result = await CreateEventUseCase(repo, uow, audit).execute(
        _concert_create(), uuid4()
    )

    repo.save.assert_called_once()
    audit.log.assert_called_once()
    uow.commit.assert_called_once()
    assert result.event_type == "concert"


async def test_create_event_slug_existe(
    repo: AsyncMock, uow: AsyncMock, audit: AsyncMock
) -> None:
    repo.find_by_slug.return_value = _make_event()

    with pytest.raises(EventSlugAlreadyExistsException):
        await CreateEventUseCase(repo, uow, audit).execute(_concert_create(), uuid4())

    repo.save.assert_not_called()
    audit.log.assert_not_called()


# ── GetEventUseCase ───────────────────────────────────────────────────────────


async def test_get_event_introuvable(repo: AsyncMock) -> None:
    repo.find_by_public_id.return_value = None

    with pytest.raises(EventNotFoundException):
        await GetEventUseCase(repo).execute(uuid4())


async def test_get_event_succes(repo: AsyncMock) -> None:
    event = _make_event()
    repo.find_by_public_id.return_value = event

    result = await GetEventUseCase(repo).execute(event.public_id)
    assert result.slug == event.slug


# ── DeleteEventUseCase ────────────────────────────────────────────────────────


async def test_delete_event_succes(
    repo: AsyncMock, uow: AsyncMock, audit: AsyncMock
) -> None:
    event = _make_event()
    repo.find_by_public_id.return_value = event

    await DeleteEventUseCase(repo, uow, audit).execute(event.public_id, uuid4())

    repo.delete.assert_called_once_with(event)
    audit.log.assert_called_once()
    uow.commit.assert_called_once()


async def test_delete_event_introuvable(
    repo: AsyncMock, uow: AsyncMock, audit: AsyncMock
) -> None:
    repo.find_by_public_id.return_value = None

    with pytest.raises(EventNotFoundException):
        await DeleteEventUseCase(repo, uow, audit).execute(uuid4(), uuid4())