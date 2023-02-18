from geopy.distance import geodesic, Distance
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from .city import City
from .coordinate import Coordinate
from .entity import Entity, get_foreign_key, LAZY_MODE


class Road(Entity):
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    city_id: int = Column(Integer, get_foreign_key(City), nullable=False)
    point_0_id: int = Column(Integer, get_foreign_key(Coordinate), nullable=False)
    point_1_id: int = Column(Integer, get_foreign_key(Coordinate), nullable=False)

    city: City = relationship(City, lazy=LAZY_MODE)
    # TODO: внешние ключи захардкодены
    point_0: Coordinate = relationship(Coordinate, lazy=LAZY_MODE, foreign_keys='Road.point_0_id')
    point_1: Coordinate = relationship(Coordinate, lazy=LAZY_MODE, foreign_keys='Road.point_1_id')

    @property
    def length(self) -> Distance:
        coordinate_0 = self.point_0.latitude, self.point_0.longitude
        coordinate_1 = self.point_1.latitude, self.point_1.longitude
        return geodesic(coordinate_0, coordinate_1)

    # noinspection PyTypeChecker
    def as_segment(self) -> tuple[float, float, float, float]:
        return *self.point_0.as_point(), *self.point_1.as_point()
