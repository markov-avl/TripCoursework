from typing import Sequence

from flask import abort

from entity import Place, City, Coordinate
from repository import PlaceRepository
from service import CoordinateService


class PlaceService:
    def __init__(self):
        self._place_repository = PlaceRepository()
        self._coordinate_service = CoordinateService()

    def get_all(self) -> Sequence[Place]:
        return self._place_repository.find_all()

    def get_by_id(self, id_: int) -> Place:
        if place := self._place_repository.find_by_id(id_):
            return place
        abort(404)

    def create(self,
               city: City,
               coordinate: Coordinate,
               name: str,
               address: str) -> Place:
        place = Place(
            city_id=city.id,
            coordinate_id=coordinate.id,
            name=name,
            address=address
        )
        self._place_repository.save(place)
        return place

    def create_with_coordinates(self,
                                city: City,
                                latitude: float,
                                longitude: float,
                                name: str,
                                address: str) -> Place:
        coordinate = self._coordinate_service.create(latitude, longitude)
        return self.create(city, coordinate, name, address)
