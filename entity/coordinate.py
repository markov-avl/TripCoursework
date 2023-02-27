from __future__ import annotations

from geopy.distance import Distance, geodesic
from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import Relationship, relationship

from .city import City
from .entity import Entity, get_foreign_key, LAZY_MODE


class Coordinate(Entity):
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    city_id: int = Column(Integer, get_foreign_key(City), nullable=False)
    longitude: float = Column(Float, nullable=False)
    latitude: float = Column(Float, nullable=False)

    city: City | Relationship = relationship(City, lazy=LAZY_MODE)

    @property
    def point(self) -> tuple[float, float]:
        return self.longitude, self.latitude

    def distance(self, coordinate: Coordinate) -> float:
        return ((self.longitude - coordinate.longitude) ** 2 + (self.latitude - coordinate.latitude) ** 2) ** 0.5

    def geo_distance(self, coordinate: Coordinate) -> Distance:
        return geodesic((self.latitude, self.longitude), (coordinate.latitude, coordinate.longitude))
