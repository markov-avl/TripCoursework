from typing import Any, Sequence

from sqlalchemy import select, or_, and_

from entity import Coordinate, City, Road, Place
from .repository import Repository


class CoordinateRepository(Repository):
    def __init__(self):
        super().__init__(Coordinate)

    def find_all(self) -> Sequence[Coordinate]:
        return super().find_all()

    def find_by(self, condition: Any) -> Sequence[Coordinate]:
        return super().find_by(condition)

    def find_by_id(self, id_: int) -> Coordinate | None:
        return super().find_by_id(id_)

    def find_by_city_left_joined_place_where_place_coordinate_is_null(self, city: City) -> Sequence[Coordinate]:
        statement = (
            select(self._entity_type).
            join(Place, Place.coordinate_id == Coordinate.id, isouter=True).
            where(and_(Coordinate.city == city, Place.coordinate == None))
        )
        return super()._fetch_all(statement)

    def find_by_city_joined_road_ordered_by_id(self, city: City) -> Sequence[tuple[Coordinate, Road]]:
        statement = (
            select(self._entity_type, Road).
            join(Road, Road.point_0_id == Coordinate.id).
            where(Coordinate.city == city).
            order_by(Coordinate.id)
        )
        return super()._fetch_all(statement, scalar=False)

    def find_by_city_joined_road_with_repetitions_ordered_by_id(self, city: City) -> Sequence[tuple[Coordinate, Road]]:
        statement = (
            select(self._entity_type, Road).
            join(Road, or_(Road.point_0_id == Coordinate.id, Road.point_1_id == Coordinate.id)).
            where(Coordinate.city == city).
            order_by(Coordinate.id)
        )
        return super()._fetch_all(statement, scalar=False)
