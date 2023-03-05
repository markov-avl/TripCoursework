from io import BytesIO
from itertools import groupby, chain
from typing import Sequence, Iterable

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

    def print_map(self, with_roads=True, with_places=True, with_ids=True) -> BytesIO:
        roads = self._road_service.get_by_city(self._city) if with_roads else []
        places = self._place_service.get_by_city(self._city) if with_places else []
        figure, axis, basemap = self._get_plot(self._to_coordinates(places))

        self._print_roads(axis, basemap, roads, segments=with_roads, points=with_ids, ids=with_ids)
        self._print_places(axis, basemap, places, points=with_places, ids=with_ids)

        return self._get_image(figure)

    def print_city_roads(self) -> BytesIO:
        coordinates = self._coordinate_service.get_by_city_which_not_places(self._city)
        figure, axis, basemap = self._get_plot(coordinates)

        background = dict(c='black', marker='D', s=3, linewidths=0, alpha=0.7)
        foreground = dict(c='white', fontsize=1, va='center', ha='center')
        self._print_coordinates(axis, basemap, coordinates, background, foreground)

        return self._get_image(figure)

    def print_city_places(self) -> BytesIO:
        places = self._place_service.get_by_city(self._city)
        figure, axis, basemap = self._get_plot(self._to_coordinates(places))

        self._print_places(axis, basemap, places, points=True, ids=True)

        return self._get_image(figure)

    def print_shortest_path(self, shortest_path: ShortestPath) -> BytesIO:
        places = [shortest_path.start, shortest_path.destination]
        figure, axis, basemap = self._get_plot(self._to_coordinates(places))

        self._print_places(axis, basemap, places)
        self._print_path(basemap, shortest_path.points, 'green')

        rounding = 3
        info = '\n'.join([
            f'Footpath distance: {round(shortest_path.footpath_distance.km, rounding)} km',
            f'Highway distance: {round(shortest_path.highway_distance.km, rounding)} km',
            f'Distance: {round(shortest_path.distance.km, rounding)} km',
            f'Straight distance: {round(shortest_path.straight_distance.km, rounding)} km'
        ])
        plt.text(0, 1.01, info, ha='left', va='bottom', fontsize=4, transform=axis.transAxes)

        return self._get_image(figure)

    def _get_plot(self, coordinates: Iterable[Coordinate] = None) -> tuple[Figure, Axes, Basemap]:
        graph = self._coordinate_service.get_by_city_with_adjacent_roads_with_repetitions(self._city)

        longitudes: set[float] = {
            *chain.from_iterable((c.longitude, r.point_0.longitude, r.point_1.longitude) for c, r in graph),
            *([c.longitude for c in coordinates] if coordinates else [])
        }
        latitudes: set[float] = {
            *chain.from_iterable((c.latitude, r.point_0.latitude, r.point_1.latitude) for c, r in graph),
            *([c.latitude for c in coordinates] if coordinates else [])
        }

        min_lon, max_lon, center_lon = self._get_longitudes(longitudes)
        min_lat, max_lat, center_lat = self._get_latitudes(latitudes)
        w, h = self._get_size(min_lat, max_lat, min_lon, max_lon)

        figure, axis = plt.subplots(frameon=False)
        axis.axis('off')
        basemap = Basemap(projection=self._projection, lon_0=center_lon, lat_0=center_lat, width=w, height=h)

        self._print_graph(axis, basemap, graph)

        return figure, axis, basemap

    def _get_image(self, figure: Figure) -> BytesIO:
        image = BytesIO()
        params = dict(dpi=800.0, format='png', bbox_inches='tight', pad_inches=0)
        figure.savefig(image, **params)
        return image

    def _print_path(self, m: Basemap, coordinates: Sequence[Coordinate], color: str = 'black') -> None:
        x = [coordinate.longitude for coordinate in coordinates]
        y = [coordinate.latitude for coordinate in coordinates]
        m.plot(x, y, latlon=True, color=color, linewidth=0.2)

    def _print_graph(self, axis: Axes, basemap: Basemap, graph: Sequence[tuple[Coordinate, Road]]) -> None:
        for coordinate, grouped in groupby(graph, key=lambda g: g[0]):
            roads: list[Road] = [group[1] for group in grouped]
            if len(roads) == 2:
                self._print_cross_way(axis, basemap, coordinate, roads)
            else:
                for road in roads:
                    self._print_one_way(axis, basemap, coordinate, road)
        basemap.plot([], [])

    def _print_one_way(self, axis: Axes, basemap: Basemap, coordinate: Coordinate, road: Road) -> None:
        vertices = [basemap(*road.center), basemap(*coordinate.point)]
        codes = [path.Path.MOVETO, path.Path.LINETO]
        rounded_verts = patches.PathPatch(path.Path(vertices, codes), fill=False, lw=0.2)
        axis.add_patch(rounded_verts)

    def _print_cross_way(self, axis: Axes, basemap: Basemap, coordinate: Coordinate, roads: list[Road]) -> None:
        roads = roads.copy()

        while len(roads) > 1:
            for i in range(1, len(roads)):
                vertices = [basemap(*roads[0].center), basemap(*coordinate.point), basemap(*roads[i].center)]
                codes = [path.Path.MOVETO, path.Path.CURVE3, path.Path.CURVE3]

                segment = *roads[0].center, *coordinate.point
                if intersections := self._segment_circle_intersection(segment, coordinate.point, self._radius):
                    vertices.insert(1, basemap(*intersections[0]))
                    codes.insert(1, path.Path.LINETO)

                segment = *roads[i].center, *coordinate.point
                if intersections := self._segment_circle_intersection(segment, coordinate.point, self._radius):
                    vertices.insert(-1, basemap(*intersections[0]))
                    codes.append(path.Path.LINETO)

                rounded_vertices = patches.PathPatch(path.Path(vertices, codes), fill=False, lw=0.2)
                axis.add_patch(rounded_vertices)
            roads.pop(0)

    def _print_roads(self,
                     axis: Axes,
                     basemap: Basemap,
                     roads: Iterable[Road],
                     segments=True,
                     points=True,
                     ids=False) -> None:
        if segments:
            params = dict(c='black', linewidth=0.2)
            for road in roads:
                x = road.point_0.longitude, road.point_1.longitude
                y = road.point_0.latitude, road.point_1.latitude
                basemap.plot(x, y, latlon=True, **params)
        if points or ids:
            coordinates = self._to_coordinates(roads)
            background = dict(c='black', marker='D', s=3, linewidths=0, alpha=0.7) if points else None
            foreground = dict(c='red', fontsize=1, va='center', ha='center') if ids else None
            if background and ids:
                foreground['c'] = 'white'
            self._print_coordinates(axis, basemap, coordinates, background, foreground)

    def _print_places(self, axis: Axes, basemap: Basemap, places: Iterable[Place], points=True, ids=False) -> None:
        if points or ids:
            coordinates = self._to_coordinates(places)
            background = dict(c='blue', marker='.', s=15, linewidths=0, alpha=0.7) if points else None
            foreground = dict(c='red', fontsize=1, va='center', ha='center') if ids else None
            if background and ids:
                foreground['c'] = 'white'
            self._print_coordinates(axis, basemap, coordinates, background, foreground)

    def _print_coordinates(self,
                           axis: Axes,
                           basemap: Basemap,
                           coordinates: Iterable[Coordinate],
                           background: dict = None,
                           foreground: dict = None) -> None:
        for coordinate in coordinates if background or foreground else []:
            x, y = basemap(*coordinate.point)
            if background:
                axis.scatter(x, y, **background)
            if foreground:
                axis.text(x, y, str(coordinate.id), **foreground)

    @staticmethod
    def _to_coordinates(entities: Iterable[Road | Place]) -> set[Coordinate]:
        return set(chain.from_iterable((e.point_0, e.point_1)
                                       if isinstance(e, Road) else (e.coordinate,) for e in entities))

    @staticmethod
    def _to_longitudes(coordinates: Iterable[Coordinate]) -> list[float]:
        return [c.longitude for c in coordinates]

    @staticmethod
    def _to_latitudes(coordinates: Iterable[Coordinate]) -> list[float]:
        return [c.latitude for c in coordinates]

    @staticmethod
    def _get_longitudes(longitudes: Iterable[float]) -> tuple[float, float, float]:
        min_ = min(longitudes)
        max_ = max(longitudes)
        return min_, max_, (min_ + max_) / 2

    @staticmethod
    def _get_latitudes(latitudes: Iterable[float]) -> tuple[float, float, float]:
        min_ = min(latitudes)
        max_ = max(latitudes)
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
