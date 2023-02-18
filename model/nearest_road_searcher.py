from entity import Place, Road
from service import RoadService


class NearestRoadSearcher:
    def __init__(self):
        self._road_service = RoadService()

    def find(self, place: Place) -> list[Road]:
        roads = self._road_service.get_by_city(place.city)
        point = place.coordinate.as_point()

        distances: dict[float, list[Road]] = {}
        for road in roads:
            segment = road.as_segment()
            current_distance = self._distance(point, segment)
            if current_distance not in distances:
                distances[current_distance] = []
            distances[current_distance].append(road)

        return distances[min(distances.keys())] if len(distances) > 1 else next(iter(distances.values()), [])

    @staticmethod
    def _distance(point: tuple[float, float], segment: tuple[float, float, float, float]) -> float:
        px1, py1 = point
        sx1, sy1, sx2, sy2 = segment

        px = sx2 - sx1
        py = sy2 - sy1

        u = ((px1 - sx1) * px + (py1 - sy1) * py) / (px ** 2 + py ** 2)

        if u > 1:
            u = 1
        elif u < 0:
            u = 0

        return ((u * px + sx1 - px1) ** 2 + (u * py + sy1 - py1) ** 2) ** .5
