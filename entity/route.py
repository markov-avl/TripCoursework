from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .city import City
from .entity import Entity, get_foreign_key, LAZY_MODE


class Route(Entity):
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    city_id: int = Column(Integer, get_foreign_key(City), nullable=False)
    secret: str = Column(String(length=16), unique=True, nullable=False)
    starts_at: datetime = Column(DateTime(timezone=True), nullable=False)
    ends_at: datetime = Column(DateTime(timezone=True), nullable=False)

    city: City = relationship(City, lazy=LAZY_MODE)

    def __init__(self,
                 city: int | City = None,
                 secret: str = None,
                 starts_at: datetime = None,
                 ends_at: datetime = None):
        if isinstance(city, int):
            self.city_id = city
        if isinstance(city, City):
            self.city = city
        self.secret = secret
        self.starts_at = starts_at
        self.ends_at = ends_at
