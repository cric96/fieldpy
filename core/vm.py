from abc import abstractmethod, ABC
from typing import List, Tuple, Dict, Any, Callable, TypeVar, Generic, Iterable
from core import Export, Path, Slot


class VMStatus:
    def __init__(self, path: Path = Path(), index: int = 0, stack: List[Tuple[Path, int]] = None):
        if stack is None:
            stack = []
        self.path = path
        self.index = index
        self.stack = stack

    def nest(self, s: Slot):
        self.path = self.path.push(s)
        self.index = 0
        return self

    def increment_index(self):
        self.index += 1
        return self

    def push(self):
        self.stack = [(self.path, self.index)] + self.stack
        return self

    def pop(self):
        if self.stack:
            path, index = self.stack[0]
            self.stack = self.stack[1:]
            self.path = path
            self.index = index
        else:
            raise Exception("Stack is empty")
        return self


class VM:
    def __init__(self, context):
        self.context = context
        self.status = VMStatus(Path())
        self.out_exports = {}

    def reset(self, context):
        self.out_exports = {}
        self.context = context
        self.status = VMStatus(Path())

    def enter(self, tag):
        index = self.status.index
        slot = Slot(tag, index)
        self.status = self.status.push().nest(slot)

    def send(self, data):
        to_send = [(id, local, self.out_exports.get(id, Export())) for id, local in data.items()]
        for _, local, export_data in to_send:
            export_data.put(self.status.path, local)
        self.out_exports.update({id: export_data for id, _, export_data in to_send})

    def store(self, local):
        self.send({self.context.id: local})

    @property
    def received(self) -> Dict[int, Any]:
        path = self.status.path
        return {nid: export_data.get(path) for nid, export_data in self.context.exports.items() if
                path in export_data.paths}

    def neighbors_aligned(self) -> Iterable[int]:
        return self.received.keys()

    def exit(self):
        self.status = self.status.pop().increment_index()

T = TypeVar('T')
A = TypeVar('A')


class Field(Generic[T]):
    def __init__(self, vm: VM, data: Dict[int, T]):
        """
        Initialize a Field object.

        Args:
            vm (VM): The VM object associated with the field.
            data (Dict[int, T]): The data dictionary containing values for each node ID.
        """
        self.vm = vm
        self.data = data

    @property
    def local(self) -> T:
        """
        Get the local value of the field for the current node.

        Returns:
            T: The local value of the field.
        """
        return self.data.get(self.vm.context.id)

    def current_aligned_without_self(self) -> Dict[int, T]:
        """
        Get the values of the field for the aligned neighbors, excluding the current node.

        Returns:
            Dict[int, T]: The values of the field for the aligned neighbors.
        """
        neighbors = self.vm.neighbors_aligned()
        return {nid: self.data.get(nid) for nid in neighbors if nid != self.vm.context.id}

    def hood(self, default: T, operation: Callable[[Tuple[A, T]], T]) -> A:
        """
        Perform a neighborhood operation on the field values.

        Args:
            default (T): The default value to return if there are no aligned neighbors.
            operation (Callable[[Tuple[A, T]], T]): The operation to perform on each neighbor value.

        Returns:
            A: The result of the neighborhood operation.
        """
        current_neigh = self.current_aligned_without_self()
        if not current_neigh:
            return default

        acc = None
        for nid, value in current_neigh.items():
            acc = value if acc is None else operation((nid, self.vm.received.get(nid)))
        return acc

    def fold(self, default: T, operation: Callable[[T, T], T]) -> T:
        """
        Perform a fold operation on the field values.

        Args:
            default (T): The default value to start the fold operation.
            operation (Callable[[T, T], T]): The operation to perform on each value during the fold.

        Returns:
            T: The result of the fold operation.
        """
        current_neigh = self.current_aligned_without_self()
        acc = default
        for value in current_neigh.values():
            acc = operation(acc, value)
        return acc

    def without_self(self):
        """
        Create a new Field object without the value of the current node.

        Returns:
            Field: A new Field object without the value of the current node.
        """
        return Field(self.vm, {nid: value for nid, value in self.data.items() if nid != self.vm.context.id})

    def __repr__(self):
        return str(self.data)

class Context(ABC):
    @abstractmethod
    def neighbours(self) -> List[int]:
        pass

    @abstractmethod
    def sensorData(self, what: str) -> Any:
        pass

    @abstractmethod
    def neighboringSensorData(self, what: str) -> Field[Any]:
        pass

    