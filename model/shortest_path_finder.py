from typing import Sequence

from networkx import Graph, dijkstra_path

from entity import Place, Road, Coordinate, City
from service import CoordinateService, RoadService

from .shortest_path import ShortestPath


class ShortestPathFinder:
    def __init__(self, city: City):
        self._city = city
        self._road_service = RoadService()
        self._coordinate_service = CoordinateService()

    def find(self, start: Place, destination: Place) -> ShortestPath:
        if self._city != start.city or self._city != destination.city:
            raise ValueError(f'Places are not in city of `{self._city.name}`')

        roads = self._road_service.get_by_city(self._city)
        start_nearest_roads = self.find_nearest_roads(start, roads)
        destination_nearest_roads = self.find_nearest_roads(destination, roads)
        start_point = self._get_vertex(start.coordinate, start_nearest_roads)
        destination_point = self._get_vertex(destination.coordinate, destination_nearest_roads)

        graph_roads = self._coordinate_service.get_by_city_with_adjacent_roads(self._city)
        graph = Graph()

        for coordinate, road in graph_roads:
            point = road.point_0 if road.point_0_id != coordinate.id else road.point_1
            if road in start_nearest_roads and len(start_nearest_roads) == 1:
                graph.add_edge(coordinate, start_point, weight=coordinate.distance(start_point))
                graph.add_edge(start_point, point, weight=start_point.distance(point))
            elif road in destination_nearest_roads and len(destination_nearest_roads) == 1:
                graph.add_edge(coordinate, destination_point, weight=coordinate.distance(destination_point))
                graph.add_edge(destination_point, point, weight=destination_point.distance(point))
            else:
                graph.add_edge(coordinate, point, weight=coordinate.distance(point))

        points = dijkstra_path(graph, start_point, destination_point)

        return ShortestPath(start, destination, points if len(points) > 1 else [])

    def find_nearest_roads(self, place: Place, roads: Sequence[Road] = None) -> list[Road]:
        if not roads:
            roads = self._road_service.get_by_city(place.city)

        distances: dict[float, list[Road]] = {}
        for road in roads:
            current_distance = road.distance(place.coordinate)
            if current_distance not in distances:
                distances[current_distance] = []
            distances[current_distance].append(road)

        return distances[min(distances.keys())] if len(distances) > 1 else next(iter(distances.values()), [])

    @staticmethod
    def _get_vertex(point: Coordinate, edges: list[Road]) -> Coordinate:
        if len(edges) == 1:
            return edges[0].nearest_point(point)
        return edges[0].point_0 if edges[0].point_0 in (edges[1].point_0, edges[1].point_1) else edges[0].point_1
