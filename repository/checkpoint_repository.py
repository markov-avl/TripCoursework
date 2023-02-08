from typing import Any, Sequence

from entity import Checkpoint
from .repository import Repository


class CheckpointRepository(Repository):
    def __init__(self):
        super().__init__(Checkpoint)

    def find_all(self) -> Sequence[Checkpoint]:
        return super().find_all()

    def find_by(self, condition: Any) -> Sequence[Checkpoint]:
        return super().find_by(condition)

    def find_by_id(self, id_: int) -> Checkpoint | None:
        return super().find_by_id(id_)
