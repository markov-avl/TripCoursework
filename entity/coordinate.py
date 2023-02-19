from __future__ import annotations

from geopy.distance import Distance, geodesic
from sqlalchemy import Column, Integer, Float

from .entity import Entity


class Coordinate(Entity):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    latitude: float = Column(Float, nullable=False)
    longitude: float = Column(Float, nullable=False)

    @property
    def point(self) -> tuple[float, float]:
        return self.latitude, self.longitude

    @property
    def reversed(self) -> tuple[float, float]:
        return self.longitude, self.latitude

    def distance(self, coordinate: Coordinate) -> float:
        return ((self.latitude - coordinate.latitude) ** 2 + (self.longitude - coordinate.longitude) ** 2) ** 0.5

    def geo_distance(self, coordinate: Coordinate) -> Distance:
        return geodesic(self.point, coordinate.point)
