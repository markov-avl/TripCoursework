from io import BytesIO
from itertools import groupby
from typing import Sequence

import numpy as np
from geopy.distance import geodesic
from matplotlib import path, patches
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap

from entity import Road, Place, City, Coordinate
from service import RoadService, PlaceService, CoordinateService

from .shortest_path import ShortestPath


class MapVisualizer:
    def __init__(self, city: City):
        self._city = city
        self._road_service = RoadService()
        self._place_service = PlaceService()
        self._coordinate_service = CoordinateService()
        self._projection = 'gnom'
        self._radius = 0.0004
        self._line_weight = 0.2

    def print_map(self, with_roads: bool = True, with_places: bool = True, with_ids: bool = True) -> BytesIO:
        image = BytesIO()

        roads = self._road_service.get_by_city(self._city) if with_roads else []
        places = self._place_service.get_by_city(self._city) if with_places else []

        if not roads and not places:
            return image

        fig, ax, m = self._get_plot(roads, places)

        self._print_graph(ax, m)
        self._print_places(m, places, with_ids)

        fig.savefig(image, dpi=800.0, format='png', bbox_inches='tight', pad_inches=0)

        return image

    def print_nearest_roads(self, place: Place, nearest_roads: Sequence[Road], with_ids: bool = True) -> BytesIO:
        roads = self._road_service.get_by_city(self._city)
        places = [place]

        fig, ax, m = self._get_plot(roads, places)

        self._print_roads(m, roads, with_ids)
        self._print_roads(m, nearest_roads, with_ids, 'green')
        self._print_places(m, places, with_ids)

        image = BytesIO()
        fig.savefig(image, dpi=800.0, format='png', bbox_inches='tight', pad_inches=0)

        return image

    def print_shortest_path(self, shortest_path: ShortestPath) -> BytesIO:
        roads = self._road_service.get_by_city(self._city)
        places = [shortest_path.start, shortest_path.destination]

        fig, ax, m = self._get_plot(roads, places)

        self._print_roads(m, roads, False)
        self._print_places(m, places, False)
        self._print_path(m, shortest_path.points, 'green')

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

    def _get_plot(self, roads: Sequence[Road], places: Sequence[Place]) -> tuple[Figure, Axes, Basemap]:
        min_longitude, max_longitude, center_longitude = self._get_longitudes(roads, places)
        min_latitude, max_latitude, center_latitude = self._get_latitudes(roads, places)
        w, h = self._get_size(min_latitude, max_latitude, min_longitude, max_longitude)

        fig, ax = plt.subplots(frameon=False)
        m = Basemap(projection=self._projection, lon_0=center_longitude, lat_0=center_latitude, width=w, height=h)

        return fig, ax, m

    def _print_path(self, m: Basemap, coordinates: Sequence[Coordinate], color: str = 'black') -> None:
        x = [coordinate.longitude for coordinate in coordinates]
        y = [coordinate.latitude for coordinate in coordinates]
        m.plot(x, y, latlon=True, color=color, linewidth=self._line_weight)

    def _print_graph(self, ax: Axes, m: Basemap) -> None:
        graph = self._coordinate_service.get_by_city_with_adjacent_roads_with_repetitions(self._city)

        for coordinate, grouped in groupby(graph, key=lambda g: g[0]):
            roads: list[Road] = [group[1] for group in grouped]
            if len(roads) == 1:
                self._print_one_way(ax, m, coordinate, roads[0])
            else:
                self._print_cross_way(ax, m, coordinate, roads)

        m.plot([], [])

    def _print_one_way(self, ax: Axes, m: Basemap, coordinate: Coordinate, road: Road) -> None:
        vertices = [m(*road.center), m(*coordinate.point)]
        codes = [path.Path.MOVETO, path.Path.LINETO]
        rounded_verts = patches.PathPatch(path.Path(vertices, codes), fill=False, lw=self._line_weight)
        ax.add_patch(rounded_verts)

    def _print_cross_way(self, ax: Axes, m: Basemap, coordinate: Coordinate, roads: list[Road]) -> None:
        roads = roads.copy()

        while len(roads) > 1:
            for i in range(1, len(roads)):
                vertices = [m(*roads[0].center), m(*coordinate.point), m(*roads[i].center)]
                codes = [path.Path.MOVETO, path.Path.CURVE3, path.Path.CURVE3]

                segment = *roads[0].center, *coordinate.point
                if intersections := self._segment_circle_intersection(segment, coordinate.point, self._radius):
                    vertices.insert(1, m(*intersections[0]))
                    codes.insert(1, path.Path.LINETO)

                segment = *roads[i].center, *coordinate.point
                if intersections := self._segment_circle_intersection(segment, coordinate.point, self._radius):
                    vertices.insert(-1, m(*intersections[0]))
                    codes.append(path.Path.LINETO)

                rounded_vertices = patches.PathPatch(path.Path(vertices, codes), fill=False, lw=self._line_weight)
                ax.add_patch(rounded_vertices)
            roads.pop(0)

    def _print_roads(self, m: Basemap, roads: Sequence[Road], with_ids: bool = False, color: str = 'black') -> None:
        for road in roads:
            x = road.point_0.longitude, road.point_1.longitude
            y = road.point_0.latitude, road.point_1.latitude
            m.plot(x, y, latlon=True, color=color, linewidth=self._line_weight)
        if with_ids:
            points: dict[int, Coordinate] = {}
            for road in roads:
                points[road.point_0.id] = road.point_0
                points[road.point_1.id] = road.point_1
            for point in points.values():
                x, y = m(*point.point)
                plt.text(x, y, point.id, fontsize=1, va='center', color='r')

    @staticmethod
    def _print_places(m: Basemap, places: Sequence[Place], with_ids: bool = False, color: str = 'red') -> None:
        x, y = m([place.coordinate.longitude for place in places], [place.coordinate.latitude for place in places])
        plt.scatter(x, y, s=0.3, color='b')
        if with_ids:
            for i, place in enumerate(places):
                plt.text(x[i], y[i], place.id, fontsize=1, va='center', color=color)

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

    @staticmethod
    def _segment_circle_intersection(segment: tuple[float, float, float, float],
                                     center: tuple[float, float],
                                     radius: float) -> list[tuple[float, float]]:
        segment_vec = segment[2] - segment[0], segment[3] - segment[1]
        displacement_vec = segment[0] - center[0], segment[1] - center[1]

        a = np.dot(segment_vec, segment_vec)
        b = 2 * np.dot(segment_vec, displacement_vec)
        c = np.dot(displacement_vec, displacement_vec) - radius ** 2
        discriminant = b ** 2 - 4 * a * c

        intersections = []

        if discriminant == 0:
            t = -b / (2 * a)
            if 0 <= t <= 1:
                intersections.append((segment[0] + t * segment_vec[0], segment[1] + t * segment_vec[1]))
        elif discriminant > 0:
            t1 = (-b + discriminant ** 0.5) / (2 * a)
            t2 = (-b - discriminant ** 0.5) / (2 * a)
            if 0 <= t1 <= 1:
                intersections.append((segment[0] + t1 * segment_vec[0], segment[1] + t1 * segment_vec[1]))
            if 0 <= t2 <= 1:
                intersections.append((segment[0] + t2 * segment_vec[0], segment[1] + t2 * segment_vec[1]))

        return intersections
