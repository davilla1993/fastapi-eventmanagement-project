from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.security.dependencies import CurrentUser, get_current_user
from app.modules.iam.api.dto.requests.auth_requests import LoginRequest, RegisterRequest
from app.modules.iam.api.dto.responses.auth_responses import TokenResponse, UserResponse
from app.modules.iam.application.usecases.login_user import LoginUserUseCase
from app.modules.iam.application.usecases.register_user import RegisterUserUseCase
from app.modules.iam.infrastructure.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un compte utilisateur",
)
async def register(
    body: RegisterRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    repo = SqlAlchemyUserRepository(db)
    return await RegisterUserUseCase(repo).execute(body)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Obtenir un token JWT",
)
async def login(
    body: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    repo = SqlAlchemyUserRepository(db)
    return await LoginUserUseCase(repo).execute(body)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Profil de l'utilisateur connecté",
)
async def me(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    from app.modules.iam.domain.exceptions.iam_exceptions import UserNotFoundException

    repo = SqlAlchemyUserRepository(db)
    user = await repo.find_by_public_id(current_user.public_id)
    if not user:
        raise UserNotFoundException(str(current_user.public_id))
    return UserResponse.model_validate(user)
