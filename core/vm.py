from typing import List, Tuple

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
    def received(self):
        path = self.status.path
        return {nid: export_data.get(path) for nid, export_data in self.context.exports.items() if path in export_data.paths}

    def exit(self):
        self.status = self.status.pop().increment_index()


class Context:
    def __init__(self, exports: dict[int, Export], id: int):
        self.exports = exports
        self.id = id

    @property
    def neighbours(self) -> List[int]:
        return list({id for id in self.exports})
