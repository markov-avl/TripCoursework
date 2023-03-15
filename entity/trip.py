from datetime import datetime, time

from sqlalchemy import Column, Integer, String, DateTime, Time
from sqlalchemy.orm import relationship, Relationship

from .place import Place
from .city import City
from .entity import Entity, get_foreign_key, LAZY_MODE


class Trip(Entity):
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    city_id: int = Column(Integer, get_foreign_key(City), nullable=True)
    accommodation_id: int = Column(Integer, get_foreign_key(Place), nullable=True)
    secret: str = Column(String(length=16), unique=True, nullable=False)
    starts_at: datetime = Column(DateTime(timezone=False), nullable=True)
    ends_at: datetime = Column(DateTime(timezone=False), nullable=True)
    awakening_at: time = Column(Time(timezone=False), nullable=True)
    resting_at: time = Column(Time(timezone=False), nullable=True)

    city: City | Relationship | None = relationship(City, lazy=LAZY_MODE)
    accommodation: Place | Relationship | None = relationship(Place, lazy=LAZY_MODE)
