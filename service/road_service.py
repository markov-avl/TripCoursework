from typing import Sequence, overload

from flask import abort

from entity import Road, City, Coordinate
from repository import RoadRepository
from service import CoordinateService


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

    def create(self,
               city: City,
               point_0: Coordinate,
               point_1: Coordinate) -> Road:
        road = Road(
            city_id=city.id,
            point_0_id=point_0.id,
            point_1_id=point_1.id
        )
        self._road_repository.save(road)
        return road

    def create_with_coordinates(self,
                                city: City,
                                point_0_latitude: float,
                                point_0_longitude: float,
                                point_1_latitude: float,
                                point_1_longitude: float) -> Road:
        point_0 = self._coordinate_service.create(point_0_latitude, point_0_longitude)
        point_1 = self._coordinate_service.create(point_1_latitude, point_1_longitude)
        return self.create(city, point_0, point_1)
