from typing import Any, Sequence

from entity import City
from .repository import Repository


class CityRepository(Repository):
    def __init__(self):
        super().__init__(City)

    def find_all(self) -> Sequence[City]:
        return super().find_all()

    def find_by(self, condition: Any) -> Sequence[City]:
        return super().find_by(condition)

    def find_by_id(self, id_: int) -> City | None:
        return super().find_by_id(id_)
