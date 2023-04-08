from datetime import datetime, time

from sqlalchemy import Column, Integer, DateTime, Float, Time
from sqlalchemy.orm import relationship, Relationship

from .visit import Visit
from .entity import Entity, get_foreign_key, LAZY_MODE


class Checkpoint(Entity):
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    visit_id: int = Column(Integer, get_foreign_key(Visit), nullable=False)
    datetime: datetime = Column(DateTime, nullable=False)
    distance: float = Column(Float, nullable=True)
    time_to_get: time = Column(Time, nullable=True)

    visit: Visit | Relationship = relationship(Visit, lazy=LAZY_MODE)
