from geopy.distance import Distance

from entity import Place, Coordinate


class ShortestPath:
    def __init__(self, start: Place, destination: Place, roads: list[Coordinate]):
        self._start = start
        self._destination = destination
        self._points = roads

    @property
    def start(self) -> Place:
        return self._start

    @property
    def destination(self) -> Place:
        return self._destination

    @property
    def points(self) -> list[Coordinate]:
        return self._points

    @property
    def footpath_distance(self) -> Distance:
        if not self._points:
            return self.straight_distance
        return self._start.coordinate.geo_distance(self._points[0]) + \
            self._destination.coordinate.geo_distance(self._points[-1])

    @property
    def highway_distance(self) -> Distance:
        distance = Distance()
        for i in range(1, len(self._points)):
            distance += self._points[i - 1].geo_distance(self._points[i])
        return distance

    @property
    def distance(self) -> Distance:
        return self.footpath_distance + self.highway_distance

    @property
    def straight_distance(self) -> Distance:
        return self._start.coordinate.geo_distance(self._destination.coordinate)
