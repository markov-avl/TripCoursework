from entity import Place, Road
from service import RoadService
from sympy import Point, Segment2D


class NearestRoad:
    def __init__(self):
        self._road_service = RoadService()

    def find(self, place: Place) -> list[Road]:
        roads = self._road_service.get_by_city(place.city)
        start_point = Point(place.coordinate.longitude, place.coordinate.latitude)
        nearest_roads = []

        p1 = Point(roads[0].edge_0.longitude, roads[0].edge_0.latitude)
        p2 = Point(roads[0].edge_1.longitude, roads[0].edge_1.latitude)
        segment = Segment2D(p1, p2)
        shortest_distance = segment.distance(start_point)

        for road in roads:
            p1 = Point(road.edge_0.longitude, road.edge_0.latitude)
            p2 = Point(road.edge_1.longitude, road.edge_1.latitude)
            segment = Segment2D(p1, p2)
            current_distance = segment.distance(start_point)

            if current_distance < shortest_distance:
                shortest_distance = current_distance
                nearest_roads = []
                nearest_roads.append(road)
            elif current_distance == shortest_distance:
                nearest_roads.append(road)

        return nearest_roads
