from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

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

    city: City = relationship(City, lazy=LAZY_MODE)
    coordinate: Coordinate = relationship(Coordinate, lazy=LAZY_MODE)

    def __init__(self,
                 city: int | City = None,
                 coordinate: int | Coordinate = None,
                 name: str = None,
                 address: str = None):
        if isinstance(city, int):
            self.city_id = city
        if isinstance(city, City):
            self.city = city
        if isinstance(coordinate, int):
            self.coordinate_id = coordinate
        if isinstance(city, Coordinate):
            self.coordinate = coordinate
        self.name = name
        self.address = address
