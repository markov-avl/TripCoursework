from typing import Any, Sequence

from entity import Place
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
