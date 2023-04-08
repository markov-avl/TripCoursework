from entity import Visit, Trip
from .route import Route


class RouteBuilder:
    def __init__(self, trip: Trip, visits: list[Visit]):
        self._trip = trip
        self._visits = visits

    def build(self) -> Route:
        ...
