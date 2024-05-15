# This is a sample Python script.
from typing import Any, List
from core import Export, Path, Slot
from core.calculus import FieldCalculus
from core.vm import VM, Context, Field


class SimpleContext(Context):
    def __init__(self, exports: dict[int, Export], id: int):
        self._exports = exports
        self.id = id


    def neighbours(self) -> List[int]:
        return list({id for id in self.exports()})

    def exports(self) -> dict[int, Export]:
        return self._exports
    def sensorData(self, what: str) -> Any:
        pass

    def neighboringSensorData(self, what: str) -> Field[Any]:
        pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    context = SimpleContext({}, 0)
    vm = VM(context)
    F = FieldCalculus(vm)

    def init():
        return 0

    def counter(old: int) -> int:
        data = F.nbr(old)
        print("NBR = " + str(data))
        return old + 1

    print(F.mid())
    print(F.rep(lambda: 0, counter))
    vm.reset(SimpleContext(vm.out_exports, 0))
    print(F.rep(lambda: 0, counter))
    vm.reset(SimpleContext(vm.out_exports, 0))
    print(F.rep(lambda: 0, counter))
