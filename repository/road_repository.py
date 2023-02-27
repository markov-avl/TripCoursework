from typing import Any, Sequence

from sqlalchemy import select, or_

from entity import Road, City, Coordinate
from .repository import Repository


class RoadRepository(Repository):
    def __init__(self):
        super().__init__(Road)

    def find_all(self) -> Sequence[Road]:
        return super().find_all()

    def find_by(self, condition: Any) -> Sequence[Road]:
        return super().find_by(condition)

    def find_by_id(self, id_: int) -> Road | None:
        return super().find_by_id(id_)

    def find_by_city(self, city: City) -> Sequence[Road]:
        statement = (
            select(self._entity_type).distinct().
            join(Coordinate, or_(Coordinate.id == Road.point_0_id, Coordinate.id == Road.point_1_id)).
            where(Coordinate.city == city).
            order_by(Coordinate.id)
        )
        return super()._fetch_all(statement)
