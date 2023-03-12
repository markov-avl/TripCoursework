from typing import Sequence

from flask import abort

from entity import Place, City, Coordinate
from repository import PlaceRepository
from .coordinate_service import CoordinateService


class PlaceService:
    def __init__(self):
        self._place_repository = PlaceRepository()
        self._coordinate_service = CoordinateService()

    def get_all(self) -> Sequence[Place]:
        return self._place_repository.find_all()

    def get_by_id(self, id_: int) -> Place:
        if place := self._place_repository.find_by_id(id_):
            return place
        abort(404, 'Место не найдено')

    def get_by_city(self, city: City) -> Sequence[Place]:
        return self._place_repository.find_by_city(city)

    def create(self, coordinate: Coordinate | int, name: str, address: str) -> Place:
        coordinate_id = coordinate if isinstance(coordinate, int) else coordinate.id

        place = Place(
            coordinate_id=coordinate_id,
            name=name,
            address=address
        )
        self._place_repository.save(place)
        return place

    def update(self,
               place: Place | int,
               coordinate: Coordinate | int = None,
               name: str = None,
               address: str = None) -> Place:
        place = self._get_entity(place)

        if coordinate:
            setattr(place, 'coordinate_id' if isinstance(coordinate, int) else 'coordinate', coordinate)
        if name:
            place.name = name
        if address:
            place.address = address

        self._place_repository.save(place)
        return place

    def delete(self, place: Place | int) -> None:
        self._place_repository.delete(self._get_entity(place))

    def create_with_coordinates(self,
                                city: City | int,
                                longitude: float,
                                latitude: float,
                                name: str,
                                address: str) -> Place:
        coordinate = self._coordinate_service.create(city, longitude, latitude)
        return self.create(coordinate, name, address)

    def _get_entity(self, place: Place | int) -> Place:
        return self.get_by_id(place) if isinstance(place, int) else place
