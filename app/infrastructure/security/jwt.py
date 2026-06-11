from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt

from app.settings import settings

_ALGORITHM = settings.algorithm


def create_access_token(subject: UUID, role: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": str(subject),
        "role": role,
        "exp": expire,
        "iat": datetime.now(UTC),
    }
    return str(jwt.encode(payload, settings.secret_key, algorithm=_ALGORITHM))


def decode_access_token(token: str) -> dict[str, str]:
    try:
        payload: dict[str, str] = jwt.decode(
            token, settings.secret_key, algorithms=[_ALGORITHM]
        )
        return payload
    except JWTError as exc:
        raise ValueError("Token invalide ou expiré.") from exc
