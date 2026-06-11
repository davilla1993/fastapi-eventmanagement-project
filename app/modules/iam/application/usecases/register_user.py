from app.infrastructure.security.password import hash_password
from app.modules.iam.api.dto.requests.auth_requests import RegisterRequest
from app.modules.iam.api.dto.responses.auth_responses import UserResponse
from app.modules.iam.domain.entities.user import User, UserRole
from app.modules.iam.domain.exceptions.iam_exceptions import EmailAlreadyExistsException
from app.modules.iam.domain.repositories.user_repository import AbstractUserRepository


class RegisterUserUseCase:
    def __init__(self, repository: AbstractUserRepository) -> None:
        self._repository = repository

    async def execute(self, request: RegisterRequest) -> UserResponse:
        existing = await self._repository.find_by_email(request.email)
        if existing:
            raise EmailAlreadyExistsException(request.email)

        user = User(
            email=request.email,
            hashed_password=hash_password(request.password),
            full_name=request.full_name,
            role=UserRole.USER,
        )
        saved = await self._repository.save(user)
        return UserResponse.model_validate(saved)
