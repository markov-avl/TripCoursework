from typing import Sequence

from flask import abort

from entity import Coordinate, City, Road
from repository import CoordinateRepository


class CoordinateService:
    def __init__(self):
        self._coordinate_repository = CoordinateRepository()

    def get_all(self) -> Sequence[Coordinate]:
        return self._coordinate_repository.find_all()

    def get_by_id(self, id_: int) -> Coordinate:
        if coordinate := self._coordinate_repository.find_by_id(id_):
            return coordinate
        abort(404)

    def get_by_city_with_adjacent_roads(self, city: City) -> Sequence[tuple[Coordinate, Road]]:
        return self._coordinate_repository.find_by_city_joined_road_ordered_by_id(city)

    def create(self, latitude: float, longitude: float) -> Coordinate:
        coordinate = Coordinate(
            latitude=latitude,
            longitude=longitude
        )
        self._coordinate_repository.save(coordinate)
        return coordinate
