from typing import Sequence

from flask import abort

from entity import Road
from repository import RoadRepository


class RoadService:
    def __init__(self):
        self._road_repository = RoadRepository()

    def get_all(self) -> Sequence[Road]:
        return self._road_repository.find_all()

    def get_by_id(self, id_: int) -> Road:
        if road := self._road_repository.find_by_id(id_):
            return road
        abort(404)
