import unittest
from core import Path, Slot, Export  # Assuming these are implemented somewhere
from core.vm import VMStatus, Field, Context, VM  # Assuming your code is in 'your_module.py'
from tests import ContextMock


class TestVMStatus(unittest.TestCase):
    def setUp(self):
        self.vm_status = VMStatus(Path())

    def test_initialization(self):
        self.assertEqual(self.vm_status.path, Path())
        self.assertEqual(self.vm_status.index, 0)
        self.assertEqual(self.vm_status.stack, [])

    def test_nest(self):
        slot = Slot("test", 0)
        self.vm_status.nest(slot)
        self.assertEqual(self.vm_status.path, Path(slot))

    def test_increment_index(self):
        self.vm_status.increment_index()
        self.assertEqual(self.vm_status.index, 1)

    def test_push(self):
        self.vm_status.push()
        self.assertEqual(len(self.vm_status.stack), 1)

    def test_pop(self):
        self.vm_status.push()
        self.vm_status.pop()
        self.assertEqual(len(self.vm_status.stack), 0)

class TestVM(unittest.TestCase):
    def setUp(self):
        self.mid = 1
        self.context = ContextMock(self.mid, {self.mid: Export()})
        self.vm = VM(self.context)

    def test_reset(self):
        self.vm.reset(self.context)
        self.assertEqual(self.vm.context, self.context)
        self.assertEqual(self.vm.status.path, Path())
        self.assertEqual(self.vm.out_exports, {})

    def test_enter(self):
        self.vm.enter("tag")
        self.assertEqual(self.vm.status.path, Path(Slot("tag", 0)))
        self.assertEqual(self.vm.status.index, 0)

    def test_send(self):
        self.vm.send({1: "local"})
        self.assertEqual(self.vm.out_exports[self.mid].get(self.vm.status.path), "local")

    def test_store(self):
        self.vm.store("local")
        self.assertEqual(self.vm.out_exports[self.mid].get(self.vm.status.path), "local")

    def test_received(self):
        self.context.exports()[self.mid].put(self.vm.status.path, "data")
        self.assertEqual(self.vm.received, {1: "data"})

    def test_neighbors_aligned(self):
        self.mid = 1
        self.context = ContextMock(self.mid, {self.mid: Export(), 2: Export(), 3: Export()})
        self.vm = VM(self.context)
        # Assuming the neighbors are 1, 2, 3, add a data
        for i in range(1, 4):
            self.context.exports()[i].put(self.vm.status.path, i)
        self.assertEqual(list(self.vm.neighbors_aligned()), [1, 2, 3])

    def test_neighbors_not_aligned(self):
        self.mid = 1
        self.context = ContextMock(self.mid, {self.mid: Export(), 2: Export(), 3: Export()})
        self.vm = VM(self.context)
        # Assuming the neighbors are 1, 2, 3, add a data
        for i in range(1, 3):
            self.context.exports()[i].put(self.vm.status.path, i)
        # Remove the data for one neighbor
        self.context.exports()[3].put(self.vm.status.path.push(Slot("foo", 0)), 3)
        self.assertEqual(list(self.vm.neighbors_aligned()), [1, 2])
    def test_exit(self):
        self.vm.enter("tag")
        self.vm.exit()
        self.assertEqual(self.vm.status.index, 1)

class TestField(unittest.TestCase):
    def setUp(self):
        self.context = ContextMock(1, {1: Export(), 2: Export({Path(): 0}), 3: Export({Path(): 0})})
        self.vm = VM(self.context)
        self.field = Field(self.vm, {1: 10, 2: 20, 3: 30})

    def test_local(self):
        self.assertEqual(self.field.local, 10)

    def test_current_aligned_without_self(self):
        self.assertEqual(self.field.current_aligned_without_self(), {2: 20, 3: 30})

    def test_hood(self):
        result = self.field.hood(0, lambda acc, x: acc + x)
        self.assertEqual(result, 60)

    def test_fold(self):
        result = self.field.fold(0, lambda acc, x: acc + x)
        self.assertEqual(result, 60)

    def test_without_self(self):
        new_field = self.field.without_self()
        self.assertEqual(new_field.data, {2: 20, 3: 30})


class TestFieldReification(unittest.TestCase):
    def setUp(self):
        export_1 = Export({Path(Slot("align", 0)): 10})
        export_2 = Export({Path(Slot("align", 0)): 20})
        export_3 = Export({Path(Slot("dealing", 0)): 30})
        self.context = ContextMock(1, {1: export_1, 2: export_2, 3: export_3})
        self.vm = VM(self.context)
        self.vm.enter("align")
        self.field = Field(self.vm, {1: 10, 2: 20, 3: 30})

    def test_local(self):
        self.assertEqual(self.field.local, 10)

    def test_current_aligned_without_self(self):
        self.assertEqual(self.field.current_aligned_without_self(), {2: 20})

    def test_hood(self):
        result = self.field.hood(0, lambda acc, x: acc + x)
        self.assertEqual(result, 30) ## 10 + 20

    def test_fold(self):
        result = self.field.fold(0, lambda acc, x: acc + x)
        self.assertEqual(result, 30) ## 10 + 20

    def empty_field(self):
        self.vm.enter("out")
        result = self.field.hood(0, lambda acc, x: acc + x)
        self.assertEqual(result, 0)

    def test_without_self(self):
        new_field = self.field.without_self()
        self.assertEqual(new_field.data, {2: 20, 3: 30})

if __name__ == '__main__':
    unittest.main()
