# This is a sample Python script.
from core import Export, Path, Slot
from core.calculus import FieldCalculus
from core.vm import VM, Context

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    context = Context({}, 0)
    vm = VM(context)
    F = FieldCalculus(vm)

    def init():
        return 0

    def counter(old: int) -> int:
        data = F.nbr(lambda: old)
        print("NBR = " + str(data))
        return old + 1

    print(F.mid())
    print(F.rep(init, counter))
    vm.reset(Context(vm.out_exports, 0))
    print(F.rep(init, counter))
    vm.reset(Context(vm.out_exports, 0))
    print(F.rep(init, counter))
