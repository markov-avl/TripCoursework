from io import BytesIO
from itertools import groupby, chain, product
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
        self._radius = 0.0005
        self._line_weight = 0.2
        self._id_params = dict(c='r', fontsize=1, ha='center', va='center')
        self._vertex_params = dict(c='black', marker='D', s=2.2, linewidths=0, alpha=0.65)
        self._image_params = dict(dpi=800.0, format='png', bbox_inches='tight', pad_inches=0)

    def print_map(self,
                  with_roads: bool = True,
                  with_places: bool = True,
                  roads_ids: bool = True,
                  places_ids: bool = True) -> BytesIO:
        image = BytesIO()

        roads = self._road_service.get_by_city(self._city) if with_roads else []
        places = self._place_service.get_by_city(self._city) if with_places else []

        if roads or places:
            fig, ax, m = self._get_plot(roads, places)

            self._print_graph(ax, m)
            self._print_places(ax, m, places)

            if roads_ids:
                self._plot_road_ids(ax, m, roads)
            if places_ids:
                self._plot_place_ids(ax, m, places)

            fig.savefig(image, **self._image_params)

        return image

    def print_nearest_roads(self, place: Place, nearest_roads: Sequence[Road], with_ids: bool = True) -> BytesIO:
        roads = self._road_service.get_by_city(self._city)
        places = [place]

        fig, ax, m = self._get_plot(roads, places)

        self._print_roads(m, roads, with_ids)
        self._print_roads(m, nearest_roads, with_ids, 'green')
        self._print_places(ax, m, places)

        image = BytesIO()
        fig.savefig(image, **self._image_params)

        return image

    def print_shortest_path(self, shortest_path: ShortestPath) -> BytesIO:
        roads = self._road_service.get_by_city(self._city)
        places = [shortest_path.start, shortest_path.destination]

        fig, ax, m = self._get_plot(roads, places)

        self._print_roads(m, roads, False)
        self._print_places(ax, m, places)
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
        fig.savefig(image, **self._image_params)

        return image

    def _get_plot(self, roads: Sequence[Road], places: Sequence[Place]) -> tuple[Figure, Axes, Basemap]:
        min_longitude, max_longitude, center_longitude = self._get_longitudes(roads, places)
        min_latitude, max_latitude, center_latitude = self._get_latitudes(roads, places)
        w, h = self._get_size(min_latitude, max_latitude, min_longitude, max_longitude)

        fig, ax = plt.subplots(frameon=False)
        ax.axis('off')

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
            if len(roads) == 2:
                self._print_cross_way(ax, m, coordinate, roads)
            else:
                for road in roads:
                    self._print_one_way(ax, m, coordinate, road)

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
    def _print_places(ax: Axes, m: Basemap, places: Sequence[Place]) -> None:
        x, y = m([place.coordinate.longitude for place in places], [place.coordinate.latitude for place in places])
        ax.scatter(x, y, s=3, linewidths=0, color='b', alpha=0.65)

    def _plot_road_ids(self, ax: Axes, m: Basemap, roads: Sequence[Road]) -> None:
        vertices = set(chain.from_iterable((road.point_0, road.point_1) for road in roads))
        self._plot_coordinate_ids(ax, m, vertices, self._vertex_params, 'w')

    def _plot_place_ids(self, ax: Axes, m: Basemap, places: Sequence[Place]) -> None:
        self._plot_coordinate_ids(ax, m, [place.coordinate for place in places], color='w')

    def _plot_coordinate_ids(self,
                             ax: Axes,
                             m: Basemap,
                             coordinates: Sequence[Coordinate],
                             background: dict = None,
                             color: str = 'r') -> None:
        self._id_params['c'] = color
        for coordinate in coordinates:
            x, y = m(*coordinate.point)
            if background:
                ax.scatter(x, y, **background)
            ax.text(x, y, coordinate.id, **self._id_params)

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
        padding = width * 1.05 - width if width >= height else height * 1.05 - height
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
