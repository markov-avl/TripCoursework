from io import BytesIO
from typing import Sequence

from geopy.distance import geodesic
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap

from entity import Road, Place


class MapVisualizer:
    @staticmethod
    def print(roads: Sequence[Road], places: Sequence[Place]) -> BytesIO:
        min_latitude, max_latitude, center_latitude = MapVisualizer._get_latitudes(roads, places)
        min_longitude, max_longitude, center_longitude = MapVisualizer._get_longitudes(roads, places)

        width, height = MapVisualizer._get_size(min_latitude, max_latitude, min_longitude, max_longitude)

        fig, ax = plt.subplots(frameon=False)
        m = Basemap(projection='gnom', lat_0=center_latitude, lon_0=center_longitude, width=width, height=height)

        bbox = dict(facecolor='w', alpha=1)

        for road in roads:
            x = [road.edge_0.longitude, road.edge_1.longitude]
            y = [road.edge_0.latitude, road.edge_1.latitude]
            m.plot(x, y, latlon=True, color='black')
            plt.text(*m(*road.center), road.id, fontsize=6, va='center', bbox=bbox)

        for place in places:
            x, y = m(place.coordinate.longitude, place.coordinate.latitude)
            plt.scatter(x, y, s=3, color='r')
            plt.text(x + 15, y, place.name, fontsize=6, va='center', bbox=bbox)

        image = BytesIO()
        fig.savefig(image, dpi=400.0, format='png', bbox_inches='tight', pad_inches=0)

        return image

    @staticmethod
    def _get_latitudes(roads: Sequence[Road], places: Sequence[Place]) -> tuple[float, float, float]:
        latitudes = [
            *[road.edge_0.latitude for road in roads],
            *[road.edge_1.latitude for road in roads],
            *[place.coordinate.latitude for place in places]
        ]
        min_ = min(latitudes)
        max_ = max(latitudes)
        return min_, max_, (min_ + max_) / 2

    @staticmethod
    def _get_longitudes(roads: Sequence[Road], places: Sequence[Place]) -> tuple[float, float, float]:
        longitudes = [
            *[road.edge_0.longitude for road in roads],
            *[road.edge_1.longitude for road in roads],
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
