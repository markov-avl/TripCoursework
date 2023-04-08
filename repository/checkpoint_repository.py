from typing import Any, Sequence

from sqlalchemy import select

from entity import Checkpoint, Trip, Visit
from .repository import Repository


class CheckpointRepository(Repository):
    def __init__(self):
        super().__init__(Checkpoint)

    def find_all(self) -> Sequence[Checkpoint]:
        return super().find_all()

    def find_by(self, condition: Any) -> Sequence[Checkpoint]:
        return super().find_by(condition)

    def find_by_id(self, id_: int) -> Checkpoint | None:
        return super().find_by_id(id_)

    def find_by_trip(self, trip: Trip | int) -> Sequence[Checkpoint]:
        trip_id = trip if isinstance(trip, int) else trip.id
        statement = (
            select(self._entity_type).
            join(Visit).
            where(Visit.trip_id == trip_id)
        )
        return self._fetch_all(statement)

    def find_by_trip_ordered_by_datetime(self, trip: Trip | int) -> Sequence[Checkpoint]:
        trip_id = trip if isinstance(trip, int) else trip.id
        statement = (
            select(self._entity_type).
            join(Visit).
            where(Visit.trip_id == trip_id).
            order_by(Checkpoint.datetime.asc())
        )
        return self._fetch_all(statement)
