from app.infrastructure.security.jwt import create_access_token
from app.infrastructure.security.password import verify_password
from app.modules.iam.api.dto.requests.auth_requests import LoginRequest
from app.modules.iam.api.dto.responses.auth_responses import TokenResponse
from app.modules.iam.domain.exceptions.iam_exceptions import (
    InactiveUserException,
    InvalidCredentialsException,
)
from app.modules.iam.domain.repositories.user_repository import AbstractUserRepository


class LoginUserUseCase:
    def __init__(self, repository: AbstractUserRepository) -> None:
        self._repository = repository

    async def execute(self, request: LoginRequest) -> TokenResponse:
        user = await self._repository.find_by_email(request.email)
        if not user or not verify_password(request.password, user.hashed_password):
            raise InvalidCredentialsException()

        if not user.is_active:
            raise InactiveUserException()

        token = create_access_token(subject=user.public_id, role=user.role.value)
        return TokenResponse(access_token=token)
