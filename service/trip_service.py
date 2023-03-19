from secrets import token_urlsafe
from datetime import date, time
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
               starts_at: date = None,
               ends_at: date = None,
               awakens_at: time = None,
               rests_at: time = None) -> Trip:
        trip = Trip(
            city_id=(city if isinstance(city, int) else city.id) if city else None,
            accommodation_id=(accommodation if isinstance(accommodation, int) else accommodation.id)
            if accommodation else None,
            secret=token_urlsafe(16),
            starts_at=starts_at,
            ends_at=ends_at,
            awakens_at=awakens_at,
            rests_at=rests_at
        )

        self._trip_repository.save(trip)
        return trip

    def update(self,
               trip: Trip | int | str,
               city: City | int = None,
               accommodation: Place | int = None,
               starts_at: date = None,
               ends_at: date = None,
               awakens_at: time = None,
               rests_at: time = None) -> Trip:
        trip = self._get_entity(trip)

        if city:
            setattr(trip, 'city_id' if isinstance(city, int) else 'city', city)
        if accommodation:
            setattr(trip, 'accommodation_id' if isinstance(accommodation, int) else 'accommodation', accommodation)
        if starts_at:
            trip.starts_at = starts_at
        if ends_at:
            trip.ends_at = ends_at
        if awakens_at:
            trip.awakens_at = awakens_at
        if rests_at:
            trip.rests_at = rests_at

        self._trip_repository.save(trip)
        return trip

    def _get_entity(self, trip: Trip | int | str) -> Trip:
        return self.get_by_id(trip) if isinstance(trip, int) else \
            (self.get_by_secret(trip) if isinstance(trip, str) else trip)
