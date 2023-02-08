from typing import Sequence

from flask import abort

from entity import Place
from repository import PlaceRepository


class PlaceService:
    def __init__(self):
        self._place_repository = PlaceRepository()

    def get_all(self) -> Sequence[Place]:
        return self._place_repository.find_all()

    def get_by_id(self, id_: int) -> Place:
        if place := self._place_repository.find_by_id(id_):
            return place
        abort(404)
