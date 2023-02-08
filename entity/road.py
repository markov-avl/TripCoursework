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
    # TODO: внешние ключи захардкодены
    edge_0: Coordinate = relationship(Coordinate, lazy=LAZY_MODE, foreign_keys='Road.edge_0_id')
    edge_1: Coordinate = relationship(Coordinate, lazy=LAZY_MODE, foreign_keys='Road.edge_1_id')
