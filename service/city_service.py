from typing import Sequence

from flask import abort

from entity import City
from repository import CityRepository


class CityService:
    def __init__(self):
        self._city_repository = CityRepository()

    def get_all(self) -> Sequence[City]:
        return self._city_repository.find_all()

    def get_by_id(self, id_: int) -> City:
        if city := self._city_repository.find_by_id(id_):
            return city
        abort(404)

    def create(self, name: str) -> City:
        city = City(
            name=name
        )
        self._city_repository.save(city)
        return city
