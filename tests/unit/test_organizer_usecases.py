"""Tests unitaires — use cases Organizer (mocks)."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.modules.iam.domain.entities.user import UserRole
from app.modules.organizers.api.dto.requests.organizer_requests import (
    OrganizerCreate,
    OrganizerUpdate,
)
from app.modules.organizers.application.usecases.create_organizer import (
    CreateOrganizerUseCase,
)
from app.modules.organizers.application.usecases.delete_organizer import (
    DeleteOrganizerUseCase,
)
from app.modules.organizers.application.usecases.get_organizer import (
    GetOrganizerUseCase,
)
from app.modules.organizers.application.usecases.update_organizer import (
    UpdateOrganizerUseCase,
)
from app.modules.organizers.domain.entities.organizer import Organizer
from app.modules.organizers.domain.exceptions.organizer_exceptions import (
    OrganizerEmailAlreadyExistsException,
    OrganizerNotFoundException,
)


def _make_organizer(**kwargs: object) -> Organizer:
    from datetime import UTC, datetime
    o = Organizer(
        name=str(kwargs.get("name", "Test Org")),
        email=str(kwargs.get("email", "test@example.com")),
    )
    o.public_id = uuid4()
    o.user_public_id = uuid4()
    o.created_at = datetime.now(UTC)
    o.updated_at = datetime.now(UTC)
    return o


@pytest.fixture
def repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def uow() -> AsyncMock:
    return AsyncMock()


# ── CreateOrganizerUseCase ────────────────────────────────────────────────────


async def test_create_organizer_succes(repo: AsyncMock, uow: AsyncMock) -> None:
    repo.find_by_email.return_value = None
    org = _make_organizer()
    repo.save.return_value = org

    request = OrganizerCreate(name="Test Org", email="test@example.com")
    result = await CreateOrganizerUseCase(repo, uow).execute(request, uuid4())

    repo.save.assert_called_once()
    uow.commit.assert_called_once()
    assert result.email == "test@example.com"


async def test_create_organizer_email_existe(repo: AsyncMock, uow: AsyncMock) -> None:
    repo.find_by_email.return_value = _make_organizer()

    request = OrganizerCreate(name="Test Org", email="duplicate@example.com")
    with pytest.raises(OrganizerEmailAlreadyExistsException):
        await CreateOrganizerUseCase(repo, uow).execute(request, uuid4())

    repo.save.assert_not_called()
    uow.commit.assert_not_called()


# ── GetOrganizerUseCase ───────────────────────────────────────────────────────


async def test_get_organizer_introuvable(repo: AsyncMock) -> None:
    repo.find_by_public_id.return_value = None

    with pytest.raises(OrganizerNotFoundException):
        await GetOrganizerUseCase(repo).execute(uuid4())


async def test_get_organizer_succes(repo: AsyncMock) -> None:
    org = _make_organizer()
    repo.find_by_public_id.return_value = org

    result = await GetOrganizerUseCase(repo).execute(org.public_id)
    assert result.email == org.email


# ── UpdateOrganizerUseCase ────────────────────────────────────────────────────


async def test_update_organizer_introuvable(repo: AsyncMock, uow: AsyncMock) -> None:
    repo.find_by_public_id.return_value = None

    with pytest.raises(OrganizerNotFoundException):
        await UpdateOrganizerUseCase(repo, uow).execute(
            uuid4(), OrganizerUpdate(), uuid4(), UserRole.ADMIN
        )


# ── DeleteOrganizerUseCase ────────────────────────────────────────────────────


async def test_delete_organizer_succes(repo: AsyncMock, uow: AsyncMock) -> None:
    org = _make_organizer()
    repo.find_by_public_id.return_value = org

    await DeleteOrganizerUseCase(repo, uow).execute(org.public_id, uuid4())

    repo.delete.assert_called_once_with(org)
    uow.commit.assert_called_once()


async def test_delete_organizer_introuvable(repo: AsyncMock, uow: AsyncMock) -> None:
    repo.find_by_public_id.return_value = None

    with pytest.raises(OrganizerNotFoundException):
        await DeleteOrganizerUseCase(repo, uow).execute(uuid4(), uuid4())