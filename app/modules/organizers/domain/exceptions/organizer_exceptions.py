from app.shared.exceptions.base import AppException


class OrganizerNotFoundException(AppException):
    status_code = 404

    def __init__(self, identifier: str) -> None:
        super().__init__(f"Organisateur '{identifier}' introuvable.")


class OrganizerEmailAlreadyExistsException(AppException):
    status_code = 409

    def __init__(self, email: str) -> None:
        super().__init__(f"Un organisateur avec l'email '{email}' existe déjà.")
