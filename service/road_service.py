from typing import Sequence, overload

from flask import abort

from entity import Road, City, Coordinate
from repository import RoadRepository
from .coordinate_service import CoordinateService


class RoadService:
    def __init__(self):
        self._road_repository = RoadRepository()
        self._coordinate_service = CoordinateService()

    def get_all(self) -> Sequence[Road]:
        return self._road_repository.find_all()

    def get_by_id(self, id_: int) -> Road:
        if road := self._road_repository.find_by_id(id_):
            return road
        abort(404, 'Road not found')

    def get_by_city(self, city: City) -> Sequence[Road]:
        return self._road_repository.find_by_city(city)

    def create(self, point_0: Coordinate | int, point_1: Coordinate | int) -> Road:
        point_0_id = point_0 if isinstance(point_0, int) else point_0.id
        point_1_id = point_1 if isinstance(point_1, int) else point_1.id

        road = Road(
            point_0_id=point_0_id,
            point_1_id=point_1_id
        )
        self._road_repository.save(road)
        return road

    def update(self, road: Road | int, point_0: Coordinate | int = None, point_1: Coordinate | int = None) -> Road:
        road = self._get_entity(road)

        if point_0:
            setattr(road, 'point_0_id' if isinstance(point_0, int) else 'point_0', point_0)
        if point_1:
            setattr(road, 'point_1_id' if isinstance(point_1, int) else 'point_1', point_1)

        self._road_repository.save(road)
        return road

    def delete(self, road: Road | int) -> None:
        self._road_repository.delete(self._get_entity(road))

    def create_with_coordinates(self,
                                city: City | int,
                                point_0_longitude: float,
                                point_0_latitude: float,
                                point_1_longitude: float,
                                point_1_latitude: float) -> Road:
        point_0 = self._coordinate_service.create(city, point_0_longitude, point_0_latitude)
        point_1 = self._coordinate_service.create(city, point_1_longitude, point_1_latitude)
        return self.create(point_0, point_1)

    def _get_entity(self, road: Road | int) -> Road:
        return self.get_by_id(road) if isinstance(road, int) else road
