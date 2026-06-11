from app.modules.organizers.api.dto.responses.organizer_responses import (
    OrganizerRead,
    OrganizerReadDetail,
)
from app.modules.organizers.domain.entities.organizer import Organizer


class OrganizerMapper:
    @staticmethod
    def to_read(organizer: Organizer) -> OrganizerRead:
        return OrganizerRead.model_validate(organizer)

    @staticmethod
    def to_detail(organizer: Organizer) -> OrganizerReadDetail:
        return OrganizerReadDetail.model_validate(organizer)
