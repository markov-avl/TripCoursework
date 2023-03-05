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
        abort(404, 'Координата не найдена')

    def get_by_city_which_not_places(self, city: City) -> Sequence[Coordinate]:
        return self._coordinate_repository.find_by_city_left_joined_place_where_place_coordinate_is_null(city)

    def get_by_city_with_adjacent_roads(self, city: City) -> Sequence[tuple[Coordinate, Road]]:
        return self._coordinate_repository.find_by_city_joined_road_ordered_by_id(city)

    def get_by_city_with_adjacent_roads_with_repetitions(self, city: City) -> Sequence[tuple[Coordinate, Road]]:
        return self._coordinate_repository.find_by_city_joined_road_with_repetitions_ordered_by_id(city)

    def create(self, city: City, longitude: float, latitude: float) -> Coordinate:
        coordinate = Coordinate(
            city_id=city.id,
            longitude=longitude,
            latitude=latitude
        )
        self._coordinate_repository.save(coordinate)
        return coordinate
