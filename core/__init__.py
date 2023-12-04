from typing import Any, Dict, List, Optional, Union


class Slot:
    def __init__(self, tag, index):
        self.index = index
        self.tag = tag

    def __str__(self):
        return str((self.tag, self.index))

    def __repr__(self):
        return str(self)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Slot) and other.tag == self.tag and other.index == self.index

    def __hash__(self):
        return hash((self.tag, self.index))


class Path:
    def __init__(self, path=None):
        if path is None:
            path = []
        self.path = path

    def push(self, slot: Slot) -> 'Path':
        return Path([slot] + self.path)

    def pull(self) -> 'Path':
        return Path(self.path[1:])

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return str(self)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Path) and other.path == self.path

    def __hash__(self):
        return hash(tuple(self.path))


class Export:
    def __init__(self, map=None):
        if map is None:
            map = {}
        self.map = map

    def put(self, path: Path, value: Any) -> Any:
        self.map[path] = value
        return value

    def get(self, path: Path) -> Optional[Any]:
        return self.map.get(path)

    def root(self) -> Any:
        return self.get(Path()).get()

    @property
    def paths(self) -> Dict[Path, Any]:
        return self.map

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Export) and other.map == self.map

    def __hash__(self):
        return hash(tuple(self.map.items()))

    def __str__(self):
        return str(self.map)

    def __repr__(self):
        return str(self)
