from sqlalchemy import Column, Integer, Float

from .entity import Entity


class Coordinate(Entity):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    latitude: float = Column(Float, nullable=False)
    longitude: float = Column(Float, nullable=False)

    def __init__(self,
                 latitude: float = None,
                 longitude: float = None):
        self.latitude = latitude
        self.longitude = longitude
