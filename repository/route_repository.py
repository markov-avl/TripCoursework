from typing import Any, Sequence

from entity import Route
from .repository import Repository


class RouteRepository(Repository):
    def __init__(self):
        super().__init__(Route)

    def find_all(self) -> Sequence[Route]:
        return super().find_all()

    def find_by(self, condition: Any) -> Sequence[Route]:
        return super().find_by(condition)

    def find_by_id(self, id_: int) -> Route | None:
        return super().find_by_id(id_)
