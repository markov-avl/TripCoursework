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
        abort(404, 'Город не найден')

    def create(self, name: str) -> City:
        city = City(
            name=name
        )

        self._city_repository.save(city)
        return city

    def update(self, city: City | int, name: str = None) -> City:
        city = self._get_entity(city)

        if name:
            city.name = name

        self._city_repository.save(city)
        return city

    def delete(self, city: City | int) -> None:
        self._city_repository.delete(self._get_entity(city))

    def _get_entity(self, city: City | int) -> City:
        return self.get_by_id(city) if isinstance(city, int) else city
