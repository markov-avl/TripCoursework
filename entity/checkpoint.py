from datetime import timedelta

from sqlalchemy import Column, Integer, Interval, Float, Enum
from sqlalchemy.orm import relationship, Relationship

from .route import Route
from .place import Place
from .entity import Entity, get_foreign_key, LAZY_MODE
from .priority import Priority


class Checkpoint(Entity):
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    route_id: int = Column(Integer, get_foreign_key(Route), nullable=False)
    place_id: int = Column(Integer, get_foreign_key(Place), nullable=False)
    stay_time: timedelta = Column(Interval, nullable=False)
    money: float = Column(Float, nullable=False, default=0.0)
    priority: Priority = Column(Enum(Priority), nullable=False, default=Priority.LOWEST)

    route: Route | Relationship = relationship(Route, lazy=LAZY_MODE)
    place: Place | Relationship = relationship(Place, lazy=LAZY_MODE)
