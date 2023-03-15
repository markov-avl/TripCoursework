from secrets import token_urlsafe
from datetime import datetime, time
from typing import Sequence

from flask import abort

from entity import Trip, City, Place
from repository import TripRepository


class TripService:
    def __init__(self):
        self._trip_repository = TripRepository()

    def get_all(self) -> Sequence[Trip]:
        return self._trip_repository.find_all()

    def get_by_id(self, id_: int) -> Trip:
        if trip := self._trip_repository.find_by_id(id_):
            return trip
        abort(404, 'Путешествие не найдено')

    def get_by_secret(self, secret: str) -> Trip:
        if trip := self._trip_repository.find_by_secret(secret):
            return trip
        abort(404, 'Путешествие не найдено')

    def create(self,
               city: City | int = None,
               accommodation: Place | int = None,
               starts_at: datetime = None,
               ends_at: datetime = None,
               awakening_at: time = None,
               resting_at: time = None) -> Trip:
        city_id = (city if isinstance(city, int) else city.id) if city else None
        accommodation_id = (accommodation if isinstance(accommodation, int) else accommodation.id) \
            if accommodation else None

        trip = Trip(
            city_id=city_id,
            accommodation_id=accommodation_id,
            secret=token_urlsafe(16),
            starts_at=starts_at,
            ends_at=ends_at,
            awakening_at=awakening_at,
            resting_at=resting_at
        )

        self._trip_repository.save(trip)
        return trip
