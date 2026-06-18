from app.modules.venues.api.dto.responses.venue_responses import (
    VenueRead,
    VenueReadDetail,
)
from app.modules.venues.domain.entities.venue import Venue


class VenueMapper:
    @staticmethod
    def to_read(venue: Venue) -> VenueRead:
        return VenueRead.model_validate(venue)

    @staticmethod
    def to_detail(venue: Venue) -> VenueReadDetail:
        return VenueReadDetail.model_validate(venue)