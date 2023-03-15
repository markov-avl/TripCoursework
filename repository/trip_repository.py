from typing import Any, Sequence

from sqlalchemy import select

from entity import Trip
from .repository import Repository


class TripRepository(Repository):
    def __init__(self):
        super().__init__(Trip)

    def find_all(self) -> Sequence[Trip]:
        return super().find_all()

    def find_by(self, condition: Any) -> Sequence[Trip]:
        return super().find_by(condition)

    def find_by_id(self, id_: int) -> Trip | None:
        return super().find_by_id(id_)

    def find_by_secret(self, secret: str) -> Trip | None:
        statement = (
            select(self._entity_type).
            where(Trip.secret == secret)
        )
        return self._fetch(statement)
