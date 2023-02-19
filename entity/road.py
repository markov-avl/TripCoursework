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

    # noinspection PyTypeChecker
    @property
    def segment(self) -> tuple[float, float, float, float]:
        return *self.point_0.point, *self.point_1.point

    def distance(self, point: Coordinate) -> float:
        return self.nearest_point(point).distance(point)

    def geo_distance(self, coordinate: Coordinate) -> Distance:
        return self.nearest_point(coordinate).geo_distance(coordinate)

    def nearest_point(self, point: Coordinate) -> Coordinate:
        px = self.point_1.latitude - self.point_0.latitude
        py = self.point_1.longitude - self.point_0.longitude

        u = ((point.latitude - self.point_0.latitude) * px + (point.longitude - self.point_0.longitude) * py) \
            / (px ** 2 + py ** 2)

        if u > 1:
            u = 1
        elif u < 0:
            u = 0

        return Coordinate(
            latitude=u * px + self.point_0.latitude,
            longitude=u * py + self.point_0.longitude
        )
