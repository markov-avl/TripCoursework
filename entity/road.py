from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from .city import City
from .coordinate import Coordinate
from .entity import Entity, get_foreign_key, LAZY_MODE


class Road(Entity):
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    city_id: int = Column(Integer, get_foreign_key(City), nullable=False)
    edge_0_id: int = Column(Integer, get_foreign_key(Coordinate), nullable=False)
    edge_1_id: int = Column(Integer, get_foreign_key(Coordinate), nullable=False)

    city: City = relationship(City, lazy=LAZY_MODE)
    edge_0: Coordinate = relationship(Coordinate, lazy=LAZY_MODE)
    edge_1: Coordinate = relationship(Coordinate, lazy=LAZY_MODE)

    def __init__(self,
                 city: int | City = None,
                 edge_0: int | Coordinate = None,
                 edge_1: int | Coordinate = None):
        if isinstance(city, int):
            self.city_id = city
        if isinstance(city, City):
            self.city = city
        if isinstance(edge_0, int):
            self.edge_0_id = edge_0
        if isinstance(edge_0, Coordinate):
            self.edge_0 = edge_0
        if isinstance(edge_1, int):
            self.edge_1_id = edge_1
        if isinstance(edge_1, Coordinate):
            self.edge_1 = edge_1
