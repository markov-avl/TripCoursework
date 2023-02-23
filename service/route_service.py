from typing import Sequence

from flask import abort

from entity import Route
from repository import RouteRepository


class RouteService:
    def __init__(self):
        self._route_repository = RouteRepository()

    def get_all(self) -> Sequence[Route]:
        return self._route_repository.find_all()

    def get_by_id(self, id_: int) -> Route:
        if route := self._route_repository.find_by_id(id_):
            return route
        abort(404, 'Route not found')
