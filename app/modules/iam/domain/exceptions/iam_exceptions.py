from app.shared.exceptions.base import AppException


class UserNotFoundException(AppException):
    status_code = 404

    def __init__(self, identifier: str) -> None:
        super().__init__(f"Utilisateur '{identifier}' introuvable.")


class EmailAlreadyExistsException(AppException):
    status_code = 409

    def __init__(self, email: str) -> None:
        super().__init__(f"L'email '{email}' est déjà utilisé.")


class InvalidCredentialsException(AppException):
    status_code = 401

    def __init__(self) -> None:
        super().__init__("Email ou mot de passe incorrect.")


class InactiveUserException(AppException):
    status_code = 403

    def __init__(self) -> None:
        super().__init__("Ce compte est désactivé.")
