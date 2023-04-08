from entity import Trip, Checkpoint
from service import VisitService, CheckpointService

from .route import Route
from .route_builder import RouteBuilder
from .visit_data_validator import VisitDataValidator


class Router:
    def __init__(self, trip: Trip):
        self._trip = trip
        self._visit_service = VisitService()
        self._checkpoint_service = CheckpointService()

    def get(self) -> Route:
        if checkpoints := self._checkpoint_service.get_by_trip_ordered(self._trip):
            return Route(data=checkpoints)

        route = self._build()
        if route.success:
            return Route(data=self._save_checkpoints(route.data))
        return route

    def _build(self) -> Route:
        visits = self._visit_service.get_by_trip(self._trip)
        if errors := VisitDataValidator(self._trip, visits).validate():
            return Route(errors=errors)
        return RouteBuilder(self._trip, visits).build()

    def _save_checkpoints(self, checkpoints: list[Checkpoint]) -> list[Checkpoint]:
        return [self._checkpoint_service.create(c.visit, c.datetime, c.distance, c.time_to_get) for c in checkpoints]
