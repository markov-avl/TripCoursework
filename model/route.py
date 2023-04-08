from entity import Checkpoint


class Route:
    def __init__(self, data: list[Checkpoint] = None, errors: list[str] = None):
        self._data = data if data else []
        self._errors = errors if errors else []

    @property
    def success(self) -> bool:
        return not self._errors

    @property
    def data(self) -> list[Checkpoint]:
        return self._data

    @property
    def errors(self) -> list[str]:
        return self._errors
