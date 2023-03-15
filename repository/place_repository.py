from typing import Any, Sequence

from sqlalchemy import select

from entity import Place, City, Coordinate
from .repository import Repository


class PlaceRepository(Repository):
    def __init__(self):
        super().__init__(Place)

    def find_all(self) -> Sequence[Place]:
        return super().find_all()

    def find_by(self, condition: Any) -> Sequence[Place]:
        return super().find_by(condition)

    def find_by_id(self, id_: int) -> Place | None:
        return super().find_by_id(id_)

    def find_by_city(self, city: City | int) -> Sequence[Place]:
        condition = (Coordinate.city_id if isinstance(city, int) else Coordinate.city) == city
        statement = (
            select(self._entity_type).
            join(Coordinate, Coordinate.id == Place.coordinate_id).
            where(condition).
            order_by(Coordinate.id)
        )
        return super()._fetch_all(statement)
