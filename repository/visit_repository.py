from typing import Any, Sequence

from sqlalchemy import select

from entity import Visit, Trip
from .repository import Repository


class VisitRepository(Repository):
    def __init__(self):
        super().__init__(Visit)

    def find_all(self) -> Sequence[Visit]:
        return super().find_all()

    def find_by(self, condition: Any) -> Sequence[Visit]:
        return super().find_by(condition)

    def find_by_id(self, id_: int) -> Visit | None:
        return super().find_by_id(id_)

    def find_by_trip(self, trip: Trip | int) -> Sequence[Visit]:
        trip_id = trip if isinstance(trip, int) else trip.id
        statement = (
            select(self._entity_type).
            where(Visit.trip_id == trip_id)
        )
        return self._fetch_all(statement)
