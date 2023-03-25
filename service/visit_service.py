from datetime import date, time
from typing import Sequence

from flask import abort

from entity import Visit, Trip, Place, Priority
from repository import VisitRepository


class VisitService:
    def __init__(self):
        self._visit_repository = VisitRepository()

    def get_all(self) -> Sequence[Visit]:
        return self._visit_repository.find_all()

    def get_by_id(self, id_: int) -> Visit:
        if visit := self._visit_repository.find_by_id(id_):
            return visit
        abort(404, 'Место для посещения не найдено')

    def get_by_trip(self, trip: Trip | int) -> Sequence[Visit]:
        return self._visit_repository.find_by_trip(trip)

    def delete_by_trip(self, trip: Trip | int) -> None:
        for visit in self.get_by_trip(trip):
            self._visit_repository.delete(visit)

    def create(self,
               trip: Trip | int,
               place: Place | int,
               priority: Priority = Priority.HIGH,
               stay_time: time = None,
               date_: date = None,
               time_: time = None) -> Visit:
        visit = Visit(
            trip_id=trip if isinstance(trip, int) else trip.id,
            place_id=place if isinstance(place, int) else place.id,
            priority=priority,
            stay_time=stay_time,
            date=date_,
            time=time_
        )

        self._visit_repository.save(visit)
        return visit
