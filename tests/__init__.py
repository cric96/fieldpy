from typing import Dict

from core import Export
from core.vm import Context


class ContextMock(Context):
    def __init__(self, id, exports):
        self.id = id
        self._exports = exports

    def neighbours(self):
        return [1, 2, 3]

    def exports(self) -> Dict[int, Export]:
        return self._exports

    def sensorData(self, what):
        return f"sensor_{what}"

    def neighboringSensorData(self, what):
        return {1: f"neigh_{what}_1", 2: f"neigh_{what}_2", 3: f"neigh_{what}_3"}
