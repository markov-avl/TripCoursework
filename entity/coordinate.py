from __future__ import annotations

from geopy.distance import Distance, geodesic
from sqlalchemy import Column, Integer, Float

from .entity import Entity


class Coordinate(Entity):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    longitude: float = Column(Float, nullable=False)
    latitude: float = Column(Float, nullable=False)

    @property
    def point(self) -> tuple[float, float]:
        return self.longitude, self.latitude

    def distance(self, coordinate: Coordinate) -> float:
        return ((self.longitude - coordinate.longitude) ** 2 + (self.latitude - coordinate.latitude) ** 2) ** 0.5

    def geo_distance(self, coordinate: Coordinate) -> Distance:
        return geodesic((self.latitude, self.longitude), (coordinate.latitude, coordinate.longitude))
