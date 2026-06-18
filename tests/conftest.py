"""Fixtures partagées pour tous les tests."""

from collections.abc import AsyncGenerator
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from app.infrastructure.database.session import get_db
from app.infrastructure.security.jwt import create_access_token
from app.infrastructure.security.password import hash_password
from app.main import app
from app.modules.iam.domain.entities.user import User, UserRole
from app.settings import settings
from app.shared.domain.base import Base


@pytest.fixture(scope="session")
async def test_engine() -> AsyncGenerator[AsyncEngine]:
    """Engine de test avec NullPool — connexions fraîches, pas de conflit de loop."""
    engine = create_async_engine(settings.database_url, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def admin_token(test_engine: AsyncEngine) -> str:
    """Token JWT d'un utilisateur ADMIN créé directement en base."""
    public_id = uuid4()
    admin = User(
        email="admin@test.internal",
        hashed_password=hash_password("AdminPass123!"),
        full_name="Test Admin",
        role=UserRole.ADMIN,
    )
    admin.public_id = public_id
    async with AsyncSession(test_engine, expire_on_commit=False) as session:
        session.add(admin)
        await session.commit()
    return create_access_token(public_id, UserRole.ADMIN.value)


@pytest.fixture
async def client(test_engine: AsyncEngine) -> AsyncGenerator[AsyncClient]:
    """Client HTTP avec sessions indépendantes par requête (NullPool)."""

    async def override_get_db() -> AsyncGenerator[AsyncSession]:
        async with AsyncSession(test_engine, expire_on_commit=False) as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()