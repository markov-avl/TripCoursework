from typing import Sequence

from flask import abort

from entity import Coordinate
from repository import CoordinateRepository


class CoordinateService:
    def __init__(self):
        self._coordinate_repository = CoordinateRepository()

    def get_all(self) -> Sequence[Coordinate]:
        return self._coordinate_repository.find_all()

    def get_by_id(self, id_: int) -> Coordinate:
        if coordinate := self._coordinate_repository.find_by_id(id_):
            return coordinate
        abort(404)
