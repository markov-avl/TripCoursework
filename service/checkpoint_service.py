from datetime import datetime, time
from typing import Sequence

from flask import abort

from entity import Checkpoint, Visit, Trip
from repository import CheckpointRepository


class CheckpointService:
    def __init__(self):
        self._checkpoint_repository = CheckpointRepository()

    def get_all(self) -> Sequence[Checkpoint]:
        return self._checkpoint_repository.find_all()

    def get_by_id(self, id_: int) -> Checkpoint:
        if visit := self._checkpoint_repository.find_by_id(id_):
            return visit
        abort(404, 'Контрольная точка не найдена')

    def get_by_trip(self, trip: Trip | int) -> Sequence[Checkpoint]:
        return self._checkpoint_repository.find_by_trip(trip)

    def get_by_trip_ordered(self, trip: Trip | int) -> Sequence[Checkpoint]:
        return self._checkpoint_repository.find_by_trip_ordered_by_datetime(trip)

    def delete_by_trip(self, trip: Trip | int) -> None:
        for checkpoint in self.get_by_trip(trip):
            self._checkpoint_repository.delete(checkpoint)

    def create(self,
               visit: Visit | int,
               datetime_: datetime,
               distance: float = None,
               time_to_get: time = None) -> Checkpoint:
        checkpoint = Checkpoint(
            visit_id=visit if isinstance(visit, int) else visit.id,
            datetime=datetime_,
            distance=distance,
            time_to_get=time_to_get
        )

        self._checkpoint_repository.save(checkpoint)
        return checkpoint
