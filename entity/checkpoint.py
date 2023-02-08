from datetime import timedelta

from sqlalchemy import Column, Integer, Interval, Float, Enum
from sqlalchemy.orm import relationship

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

    route: Route = relationship(Route, lazy=LAZY_MODE)
    place: Place = relationship(Place, lazy=LAZY_MODE)

    def __init__(self,
                 route: int | Route = None,
                 place: int | Place = None,
                 stay_time: timedelta = None,
                 money: float = None,
                 priority: Priority = None):
        if isinstance(route, int):
            self.route_id = route
        if isinstance(route, Route):
            self.route = route
        if isinstance(place, int):
            self.place_id = place
        if isinstance(place, Place):
            self.place = place
        self.stay_time = stay_time
        self.money = money
        self.priority = priority
