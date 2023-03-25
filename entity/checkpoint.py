from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import relationship, Relationship

from .visit import Visit
from .entity import Entity, get_foreign_key, LAZY_MODE


class Checkpoint(Entity):
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    visit_id: int = Column(Integer, get_foreign_key(Visit), nullable=False)
    datetime: datetime = Column(DateTime, nullable=False)
    day: int = Column(Integer, nullable=False)
    number: int = Column(Integer, nullable=False)

    visit: Visit | Relationship = relationship(Visit, lazy=LAZY_MODE)
