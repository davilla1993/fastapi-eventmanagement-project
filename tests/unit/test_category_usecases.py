"""Tests unitaires — use cases Category (mocks)."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.modules.categories.api.dto.requests.category_requests import CategoryCreate
from app.modules.categories.application.usecases.create_category import (
    CreateCategoryUseCase,
)
from app.modules.categories.application.usecases.get_category import GetCategoryUseCase
from app.modules.categories.domain.entities.category import Category
from app.modules.categories.domain.exceptions.category_exceptions import (
    CategoryNotFoundException,
    CategorySlugAlreadyExistsException,
)


def _make_category(**kwargs: object) -> Category:
    from datetime import UTC, datetime
    c = Category(
        name=str(kwargs.get("name", "Jazz")),
        slug=str(kwargs.get("slug", "jazz")),
    )
    c.public_id = uuid4()
    c.created_at = datetime.now(UTC)
    c.updated_at = datetime.now(UTC)
    return c


@pytest.fixture
def repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def uow() -> AsyncMock:
    return AsyncMock()


async def test_create_category_succes(repo: AsyncMock, uow: AsyncMock) -> None:
    repo.find_by_slug.return_value = None
    cat = _make_category()
    repo.save.return_value = cat

    request = CategoryCreate(name="Jazz", slug="jazz", color="#F59E0B")
    result = await CreateCategoryUseCase(repo, uow).execute(request, uuid4())

    repo.save.assert_called_once()
    uow.commit.assert_called_once()
    assert result.name == "Jazz"


async def test_create_category_slug_existe(repo: AsyncMock, uow: AsyncMock) -> None:
    repo.find_by_slug.return_value = _make_category()

    request = CategoryCreate(name="Jazz Duplicate", slug="jazz")
    with pytest.raises(CategorySlugAlreadyExistsException):
        await CreateCategoryUseCase(repo, uow).execute(request, uuid4())

    repo.save.assert_not_called()


async def test_get_category_introuvable(repo: AsyncMock) -> None:
    repo.find_by_public_id.return_value = None

    with pytest.raises(CategoryNotFoundException):
        await GetCategoryUseCase(repo).execute(uuid4())


async def test_get_category_succes(repo: AsyncMock) -> None:
    cat = _make_category()
    repo.find_by_public_id.return_value = cat

    result = await GetCategoryUseCase(repo).execute(cat.public_id)
    assert result.slug == cat.slug