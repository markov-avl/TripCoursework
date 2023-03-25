from datetime import date, time

from sqlalchemy import Column, Integer, Enum, Date, Time
from sqlalchemy.orm import relationship, Relationship

from .trip import Trip
from .place import Place
from .entity import Entity, get_foreign_key, LAZY_MODE
from .priority import Priority


class Visit(Entity):
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    trip_id: int = Column(Integer, get_foreign_key(Trip), nullable=False)
    place_id: int = Column(Integer, get_foreign_key(Place), nullable=False)
    priority: Priority = Column(Enum(Priority), nullable=False, default=Priority.HIGH)
    stay_time: time = Column(Time, nullable=True)
    date: date = Column(Date, nullable=True)
    time: time = Column(Time, nullable=True)

    trip: Trip | Relationship = relationship(Trip, lazy=LAZY_MODE)
    place: Place | Relationship = relationship(Place, lazy=LAZY_MODE)
