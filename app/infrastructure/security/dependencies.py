from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.infrastructure.security.jwt import decode_access_token
from app.modules.iam.domain.entities.user import UserRole
from app.shared.exceptions.base import ForbiddenException, UnauthorizedException

_bearer = HTTPBearer(auto_error=False)


class CurrentUser:
    def __init__(self, public_id: UUID, role: UserRole) -> None:
        self.public_id = public_id
        self.role = role


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> CurrentUser:
    if not credentials:
        raise UnauthorizedException()
    try:
        payload = decode_access_token(credentials.credentials)
        return CurrentUser(
            public_id=UUID(payload["sub"]),
            role=UserRole(payload["role"]),
        )
    except (ValueError, KeyError) as exc:
        raise UnauthorizedException("Token invalide.") from exc


def require_role(*roles: UserRole):  # type: ignore[no-untyped-def]
    async def _check(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
    ) -> CurrentUser:
        if current_user.role not in roles:
            raise ForbiddenException()
        return current_user

    return _check


require_admin = require_role(UserRole.ADMIN)
require_organizer = require_role(UserRole.ADMIN, UserRole.ORGANIZER)
