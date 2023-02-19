from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Relationship

from .city import City
from .coordinate import Coordinate
from .entity import Entity, get_foreign_key, LAZY_MODE


class Place(Entity):
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    city_id: int = Column(Integer, get_foreign_key(City), nullable=False)
    coordinate_id: int = Column(Integer, get_foreign_key(Coordinate), nullable=False)
    name: str = Column(String, nullable=False)
    address: str = Column(String, nullable=False)

    city: City | Relationship = relationship(City, lazy=LAZY_MODE)
    coordinate: Coordinate | Relationship = relationship(Coordinate, lazy=LAZY_MODE)
