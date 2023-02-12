from sqlalchemy import Column, Integer, Float
from sympy import Point2D

from .entity import Entity


class Coordinate(Entity):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    latitude: float = Column(Float, nullable=False)
    longitude: float = Column(Float, nullable=False)

    def as_point(self) -> Point2D:
        return Point2D(self.latitude, self.longitude)
