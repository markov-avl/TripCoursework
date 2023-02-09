from typing import Any, Sequence

from entity import Road, City
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
        return self.find_by(Road.city == city)
