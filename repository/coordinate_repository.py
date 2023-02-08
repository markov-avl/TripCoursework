from typing import Any, Sequence

from entity import Coordinate
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
