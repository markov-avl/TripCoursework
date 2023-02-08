from sqlalchemy import Column, Integer, String

from .entity import Entity


class City(Entity):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, unique=True, nullable=False)
