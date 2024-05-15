from typing import Any, Dict, Optional
from collections import deque


class Slot:
    """
    The Slot class represents a slot with a tag and an index.
    It is used to identify a specific slot in an AST.

    Attributes:
        tag: An arbitrary identifier for the slot.
        index: The index of the slot.
    """

    def __init__(self, tag, index):
        """
        Constructs a new Slot with the given tag and index.

        Args:
            tag: An arbitrary identifier for the slot.
            index: The index of the slot.
        """
        self.index = index
        self.tag = tag

    def __str__(self):
        """
        Returns a string representation of the Slot.

        Returns:
            A string in the format "(tag, index)".
        """
        return str((self.tag, self.index))

    def __repr__(self):
        """
        Returns a string representation of the Slot.

        Returns:
            A string in the format "(tag, index)".
        """
        return str(self)

    def __eq__(self, other: Any) -> bool:
        """
        Checks if this Slot is equal to another Slot.

        Args:
            other: The other Slot to compare with.

        Returns:
            True if the other Slot has the same tag and index, False otherwise.
        """
        return isinstance(other, Slot) and other.tag == self.tag and other.index == self.index

    def __hash__(self):
        """
        Returns a hash value for the Slot.

        Returns:
            A hash value for the Slot, computed based on the tag and index.
        """
        return hash((self.tag, self.index))



class Path:
    """
    The Path class represents a path consisting of a deque of slots.
    It is used to identify a specific path in an AST, essential for the export mechanism and alignment.
    e.g., giving the following expression:
    def foo():
    def func1():
        return foo()
    func1()
    A path to the overall expression is [Slot('func1', 0), Slot('foo', 0)].

    Attributes:
        path: A deque of slots forming the path.
    """

    def __init__(self, path=None):
        """
        Constructs a new Path with the given deque of slots.

        Args:
            path: A deque of slots forming the path. If not provided, an empty deque is used.
        """
        if path is None:
            self.path = deque()
        else:
            self.path = deque([path])

    def push(self, slot: Slot) -> 'Path':
        """
        Adds a slot to the beginning of the path and returns a new Path.

        Args:
            slot: The slot to add.

        Returns:
            A new Path with the added slot.
        """

        new_path = self.path.copy()
        new_path.appendleft(slot)
        result = Path()
        result.path = new_path
        return result

    def pull(self) -> 'Path':
        """
        Removes the first slot from the path and returns a new Path.

        Returns:
            A new Path without the first slot.
        """
        new_path = self.path.copy()
        new_path.popleft()
        return Path(new_path)

    def __str__(self):
        """
        Returns a string representation of the Path.

        Returns:
            A string representation of the list of slots.
        """
        return str(self.path)

    def __repr__(self):
        """
        Returns a string representation of the Path.

        Returns:
            A string representation of the list of slots.
        """
        return str(list(self.path))

    def __eq__(self, other: Any) -> bool:
        """
        Checks if this Path is equal to another Path.

        Args:
            other: The other Path to compare with.

        Returns:
            True if the other Path has the same list of slots, False otherwise.
        """
        return isinstance(other, Path) and other.path == self.path

    def __hash__(self):
        """
        Returns a hash value for the Path.

        Returns:
            A hash value for the Path, computed based on the list of slots.
        """
        return hash(tuple(self.path))


class Export:
    """
    The Export class represents a mapping from paths to values.
    It is used to store and retrieve values based on their paths in the AST.
    It is the main data used to share information between different parts of the AST.

    Attributes:
        map: A dictionary mapping paths to values.
    """

    def __init__(self, map=None):
        """
        Constructs a new Export with the given map.

        Args:
            map: A dictionary mapping paths to values. If not provided, an empty dictionary is used.
        """
        if map is None:
            map = {}
        self.map = map

    def put(self, path: Path, value: Any) -> Any:
        """
        Adds a value to the map at the given path and returns the value.

        Args:
            path: The path where to add the value.
            value: The value to add.

        Returns:
            The added value.
        """
        self.map[path] = value
        return value

    def get(self, path: Path) -> Optional[Any]:
        """
        Retrieves the value at the given path from the map.

        Args:
            path: The path of the value to retrieve.

        Returns:
            The value at the given path, or None if the path is not in the map.
        """
        return self.map.get(path)

    def root(self) -> Any:
        """
        Retrieves the value at the root path from the map.

        Returns:
            The value at the root path, or None if the root path is not in the map.
        """
        return self.get(Path())

    @property
    def paths(self) -> Dict[Path, Any]:
        """
        Retrieves the map of paths to values.

        Returns:
            The map of paths to values.
        """
        return self.map

    def __eq__(self, other: Any) -> bool:
        """
        Checks if this Export is equal to another Export.

        Args:
            other: The other Export to compare with.

        Returns:
            True if the other Export has the same map, False otherwise.
        """
        return isinstance(other, Export) and other.map == self.map

    def __hash__(self):
        """
        Returns a hash value for the Export.

        Returns:
            A hash value for the Export, computed based on the map.
        """
        return hash(tuple(self.map.items()))

    def __str__(self):
        """
        Returns a string representation of the Export.

        Returns:
            A string representation of the map.
        """
        return str(self.map)

    def __repr__(self):
        """
        Returns a string representation of the Export.

        Returns:
            A string representation of the map.
        """
        return str(self)