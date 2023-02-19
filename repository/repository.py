from abc import ABC
from typing import Type, Any, Sequence

from sqlalchemy import select, Result
from sqlalchemy.sql import Select

from database import database
from entity import Entity


class Repository(ABC):
    def __init__(self, entity_type: Type[Entity]):
        self._entity_type = entity_type

    @staticmethod
    def _execute(statement: Select) -> Result:
        return database.session.execute(statement)

    @staticmethod
    def _fetch(statement: Select) -> Any:
        result = Repository._execute(statement)
        return result.scalar()

    @staticmethod
    def _fetch_all(statement: Select, scalar: bool = True) -> Sequence[Any]:
        result = Repository._execute(statement)
        # TODO: возможно всё же как-то по statement можно узнавать scalar
        return result.scalars().all() if scalar else result.all()

    @staticmethod
    def save(*entities: Entity) -> None:
        database.session.add_all(entities)
        database.session.commit()

    @staticmethod
    def delete(entity: Entity) -> None:
        database.session.delete(entity)
        database.session.commit()

    def find_all(self) -> Sequence[Any]:
        statement = select(self._entity_type)
        return self._fetch_all(statement)

    def find_by(self, condition: Any) -> Sequence[Any]:
        statement = (
            select(self._entity_type).
            where(condition)
        )
        return self._fetch_all(statement)

    def find_by_id(self, id_: int) -> Any:
        statement = (
            select(self._entity_type).
            where(self._entity_type.id == id_)
        )
        return self._fetch(statement)
