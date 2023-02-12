from entity import Place, Road
from service import RoadService


class NearestRoadSearcher:
    def __init__(self):
        self._road_service = RoadService()

    def find(self, place: Place) -> list[Road]:
        roads = self._road_service.get_by_city(place.city)
        start_point = place.coordinate.as_point()

        distances = {}
        for road in roads:
            current_distance = road.as_segment().distance(start_point)
            if current_distance not in distances:
                distances[current_distance] = []
            distances[current_distance].append(road)

        return distances[min(distances.keys())] if len(distances) > 1 else next(iter(distances.values()), [])
