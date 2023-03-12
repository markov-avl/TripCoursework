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

    def create(self, city: City | int, longitude: float, latitude: float) -> Coordinate:
        city_id = city if isinstance(city, int) else city.id

        coordinate = Coordinate(
            city_id=city_id,
            longitude=longitude,
            latitude=latitude
        )
        self._coordinate_repository.save(coordinate)
        return coordinate

    def update(self,
               coordinate: Coordinate | int,
               city: City | int = None,
               longitude: float = None,
               latitude: float = None) -> Coordinate:
        coordinate = self._get_entity(coordinate)

        if city:
            setattr(coordinate, 'city_id' if isinstance(city, int) else 'city', city)
        if longitude:
            coordinate.longitude = longitude
        if latitude:
            coordinate.latitude = latitude

        self._coordinate_repository.save(coordinate)
        return coordinate

    def delete(self, coordinate: Coordinate | int) -> None:
        self._coordinate_repository.delete(self._get_entity(coordinate))

    def _get_entity(self, coordinate: Coordinate | int) -> Coordinate:
        return self.get_by_id(coordinate) if isinstance(coordinate, int) else coordinate
