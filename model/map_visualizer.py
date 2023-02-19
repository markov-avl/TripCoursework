from io import BytesIO
from typing import Sequence

from geopy.distance import geodesic
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap

from entity import Road, Place, City, Coordinate
from service import RoadService, PlaceService

from .shortest_path import ShortestPath


class MapVisualizer:
    def __init__(self, city: City):
        self._city = city
        self._road_service = RoadService()
        self._place_service = PlaceService()

    def print(self, with_roads: bool = True, with_places: bool = True, with_ids: bool = True) -> BytesIO:
        image = BytesIO()

        roads = self._road_service.get_by_city(self._city) if with_roads else []
        places = self._place_service.get_by_city(self._city) if with_places else []

        if not roads and not places:
            return image

        min_latitude, max_latitude, center_latitude = self._get_latitudes(roads, places)
        min_longitude, max_longitude, center_longitude = self._get_longitudes(roads, places)
        width, height = self._get_size(min_latitude, max_latitude, min_longitude, max_longitude)

        fig, ax = plt.subplots(frameon=False)
        m = Basemap(projection='gnom', lat_0=center_latitude, lon_0=center_longitude, width=width, height=height)

        self._print_roads(m, roads, with_ids)
        self._print_places(m, places, with_ids)

        fig.savefig(image, dpi=800.0, format='png', bbox_inches='tight', pad_inches=0)

        return image

    def print_nearest_roads(self, place: Place, nearest_roads: Sequence[Road], with_ids: bool = True) -> BytesIO:
        roads = self._road_service.get_by_city(self._city)

        min_latitude, max_latitude, center_latitude = self._get_latitudes(roads, [place])
        min_longitude, max_longitude, center_longitude = self._get_longitudes(roads, [place])
        width, height = self._get_size(min_latitude, max_latitude, min_longitude, max_longitude)

        fig, ax = plt.subplots(frameon=False)
        m = Basemap(projection='gnom', lat_0=center_latitude, lon_0=center_longitude, width=width, height=height)

        self._print_roads(m, roads, with_ids)
        self._print_roads(m, nearest_roads, with_ids, 'green')
        self._print_places(m, [place], with_ids)

        image = BytesIO()
        fig.savefig(image, dpi=800.0, format='png', bbox_inches='tight', pad_inches=0)

        return image

    def print_shortest_path(self, shortest_path: ShortestPath) -> BytesIO:
        roads = self._road_service.get_by_city(self._city)
        places = [shortest_path.start, shortest_path.destination]

        min_latitude, max_latitude, center_latitude = self._get_latitudes(roads, places)
        min_longitude, max_longitude, center_longitude = self._get_longitudes(roads, places)
        width, height = self._get_size(min_latitude, max_latitude, min_longitude, max_longitude)

        fig, ax = plt.subplots(frameon=False)
        m = Basemap(projection='gnom', lat_0=center_latitude, lon_0=center_longitude, width=width, height=height)

        self._print_roads(m, roads, False)
        self._print_places(m, places, False)
        self._print_polygonal_chain(m, shortest_path.points, 'green')

        rounding = 3
        info = '\n'.join([
            f'Footpath distance: {round(shortest_path.footpath_distance.km, rounding)} km',
            f'Highway distance: {round(shortest_path.highway_distance.km, rounding)} km',
            f'Distance: {round(shortest_path.distance.km, rounding)} km',
            f'Straight distance: {round(shortest_path.straight_distance.km, rounding)} km'
        ])
        plt.text(0, 1.01, info, ha='left', va='bottom', fontsize=4, transform=ax.transAxes)

        image = BytesIO()
        fig.savefig(image, dpi=800.0, format='png', bbox_inches='tight', pad_inches=0)

        return image

    @staticmethod
    def _print_polygonal_chain(m: Basemap, coordinates: Sequence[Coordinate], color: str = 'black') -> None:
        x = [coordinate.longitude for coordinate in coordinates]
        y = [coordinate.latitude for coordinate in coordinates]
        m.plot(x, y, latlon=True, color=color, linewidth=0.5)

    @staticmethod
    def _print_roads(m: Basemap, roads: Sequence[Road], with_ids: bool = False, color: str = 'black') -> None:
        for road in roads:
            x = road.point_0.longitude, road.point_1.longitude
            y = road.point_0.latitude, road.point_1.latitude
            m.plot(x, y, latlon=True, color=color, linewidth=0.5)
        if with_ids:
            points: dict[int, Coordinate] = {}
            for road in roads:
                points[road.point_0.id] = road.point_0
                points[road.point_1.id] = road.point_1
            for point in points.values():
                x, y = m(point.longitude, point.latitude)
                plt.text(x, y, point.id, fontsize=1, va='center', color='r')

    @staticmethod
    def _print_places(m: Basemap, places: Sequence[Place], with_ids: bool = False, color: str = 'red') -> None:
        x, y = m([place.coordinate.longitude for place in places], [place.coordinate.latitude for place in places])
        plt.scatter(x, y, s=0.3, color='b')
        if with_ids:
            for i, place in enumerate(places):
                plt.text(x[i], y[i], place.coordinate.id, fontsize=1, va='center', color=color)

    @staticmethod
    def _get_latitudes(roads: Sequence[Road], places: Sequence[Place]) -> tuple[float, float, float]:
        latitudes = [
            *[road.point_0.latitude for road in roads],
            *[road.point_1.latitude for road in roads],
            *[place.coordinate.latitude for place in places]
        ]
        min_ = min(latitudes)
        max_ = max(latitudes)
        return min_, max_, (min_ + max_) / 2

    @staticmethod
    def _get_longitudes(roads: Sequence[Road], places: Sequence[Place]) -> tuple[float, float, float]:
        longitudes = [
            *[road.point_0.longitude for road in roads],
            *[road.point_1.longitude for road in roads],
            *[place.coordinate.longitude for place in places]
        ]
        min_ = min(longitudes)
        max_ = max(longitudes)
        return min_, max_, (min_ + max_) / 2

    @staticmethod
    def _get_width(min_latitude: float, max_latitude: float, min_longitude: float, max_longitude: float) -> int:
        if min_latitude * max_latitude <= 0.0:
            latitude = 0.0
        else:
            latitude = min_latitude if min_latitude > 0 else max_latitude
        return geodesic((latitude, min_longitude), (latitude, max_longitude)).m

    @staticmethod
    def _get_height(min_longitude: float, max_longitude: float, min_latitude: float, max_latitude: float) -> int:
        if min_longitude * max_longitude <= 0.0:
            longitude = 0.0
        else:
            longitude = min_longitude if min_longitude > 0 else max_longitude
        return geodesic((min_latitude, longitude), (max_latitude, longitude)).m

    @staticmethod
    def _get_size(min_latitude: float,
                  max_latitude: float,
                  min_longitude: float,
                  max_longitude: float) -> tuple[float, float]:
        width = MapVisualizer._get_width(min_latitude, max_latitude, min_longitude, max_longitude)
        height = MapVisualizer._get_height(min_longitude, max_longitude, min_latitude, max_latitude)
        padding = width * 1.2 - width if width >= height else height * 1.2 - height
        return width + padding, height + padding
