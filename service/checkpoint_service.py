from typing import Sequence

from flask import abort

from entity import Checkpoint
from repository import CheckpointRepository


class CheckpointService:
    def __init__(self):
        self._checkpoint_repository = CheckpointRepository()

    def get_all(self) -> Sequence[Checkpoint]:
        return self._checkpoint_repository.find_all()

    def get_by_id(self, id_: int) -> Checkpoint:
        if checkpoint := self._checkpoint_repository.find_by_id(id_):
            return checkpoint
        abort(404, 'Checkpoint not found')
