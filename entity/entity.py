import re
from typing import Type

from sqlalchemy import ForeignKey
from sqlalchemy.orm import as_declarative, declared_attr

PATTERN = re.compile(r'(?<!^)(?=[A-Z])')
LAZY_MODE = 'selectin'
PK_COLUMN = 'id'


@as_declarative()
class Entity:
    __tablename__: str
    id: int

    @declared_attr
    def __tablename__(cls):
        return PATTERN.sub('_', cls.__name__).lower()


def get_foreign_key(entity: Type[Entity], on_delete: str = 'CASCADE', on_update: str = 'CASCADE') -> ForeignKey:
    return ForeignKey(
        column=f'{entity.__tablename__}.{PK_COLUMN}',
        ondelete=on_delete,
        onupdate=on_update
    )
