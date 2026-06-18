from app.shared.exceptions.base import AppException


class VenueNotFoundException(AppException):
    status_code = 404

    def __init__(self, identifier: str) -> None:
        super().__init__(f"Salle '{identifier}' introuvable.")


class VenueSlugAlreadyExistsException(AppException):
    status_code = 409

    def __init__(self, slug: str) -> None:
        super().__init__(f"Une salle avec le slug '{slug}' existe déjà.")