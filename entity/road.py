from geopy.distance import geodesic, Distance
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship, Relationship

from .city import City
from .coordinate import Coordinate
from .entity import Entity, get_foreign_key, LAZY_MODE


class Road(Entity):
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    city_id: int = Column(Integer, get_foreign_key(City), nullable=False)
    point_0_id: int = Column(Integer, get_foreign_key(Coordinate), nullable=False)
    point_1_id: int = Column(Integer, get_foreign_key(Coordinate), nullable=False)

    city: City | Relationship = relationship(City, lazy=LAZY_MODE)
    # TODO: внешние ключи захардкодены
    point_0: Coordinate | Relationship = relationship(Coordinate, lazy=LAZY_MODE, foreign_keys='Road.point_0_id')
    point_1: Coordinate | Relationship = relationship(Coordinate, lazy=LAZY_MODE, foreign_keys='Road.point_1_id')

    @property
    def length(self) -> Distance:
        return geodesic(self.point_0.point, self.point_1.point)

    @property
    def center(self) -> tuple[float, float]:
        longitude = (self.point_0.longitude + self.point_1.longitude) / 2
        latitude = (self.point_0.latitude + self.point_1.latitude) / 2
        return longitude, latitude

    @property
    def segment(self) -> tuple[float, float, float, float]:
        return *self.point_0.point, *self.point_1.point

    def distance(self, point: Coordinate) -> float:
        return self.nearest_point(point).distance(point)

    def geo_distance(self, coordinate: Coordinate) -> Distance:
        return self.nearest_point(coordinate).geo_distance(coordinate)

    def nearest_point(self, point: Coordinate) -> Coordinate:
        a = self.point_1.longitude - self.point_0.longitude
        b = self.point_1.latitude - self.point_0.latitude

        u = (a * (point.longitude - self.point_0.longitude) + b * (point.latitude - self.point_0.latitude)) \
            / (a ** 2 + b ** 2)

        if u > 1:
            u = 1
        elif u < 0:
            u = 0

        return Coordinate(
            longitude=u * a + self.point_0.longitude,
            latitude=u * b + self.point_0.latitude
        )
