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
        condition = (Visit.trip_id if isinstance(trip, int) else Visit.trip) == trip
        statement = (
            select(self._entity_type).
            where(condition)
        )
        return self._fetch_all(statement)
