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
        abort(404)

    def get_by_city(self, city: City) -> Sequence[Road]:
        return self._road_repository.find_by_city(city)

    def create(self,
               city: City,
               edge_0: Coordinate,
               edge_1: Coordinate) -> Road:
        road = Road(
            city_id=city.id,
            edge_0_id=edge_0.id,
            edge_1_id=edge_1.id
        )
        self._road_repository.save(road)
        return road

    def create_with_coordinates(self,
                                city: City,
                                edge_0_latitude: float,
                                edge_0_longitude: float,
                                edge_1_latitude: float,
                                edge_1_longitude: float) -> Road:
        edge_0 = self._coordinate_service.create(edge_0_latitude, edge_0_longitude)
        edge_1 = self._coordinate_service.create(edge_1_latitude, edge_1_longitude)
        return self.create(city, edge_0, edge_1)
