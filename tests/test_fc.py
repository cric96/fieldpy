import unittest
from typing import Dict
from unittest.mock import MagicMock

from core import Export, Path, Slot
from core.vm import VM, Field, Context
from core.calculus import FieldCalculus  # Assuming your code is in 'your_module.py'
from tests import ContextMock


class TestFieldCalculus(unittest.TestCase):
    def next_round(self):
        self.vm.reset(ContextMock(1, self.vm.out_exports))
    def setUp(self):
        # Mocking the VM and Context
        self.context = ContextMock(1, {1: Export(), 2: Export(), 3: Export()})
        self.context.id = 1
        self.context.neighbours = [2, 3]
        self.vm = VM(self.context)

        # Initializing FieldCalculus with the mocked VM
        self.field_calculus = FieldCalculus(self.vm)

    def test_rep_initialization(self):
        init = MagicMock(return_value="initial_value")
        update = MagicMock(return_value="updated_value")
        result = self.field_calculus.rep(init, update)
        self.next_round()
        self.field_calculus.rep(init, update)
        init.assert_called_once()
        self.assertEqual(result, "initial_value")

    def test_rep_update(self):
        init = MagicMock(retun_value="initial_value")
        update = MagicMock(return_value="updated_value")
        self.field_calculus.rep(init, update)
        update.assert_not_called()
        self.next_round()
        result = self.field_calculus.rep(init, update)
        update.assert_called_once()
        self.assertEqual(result, "updated_value")

    def test_mid(self):
        result = self.field_calculus.mid()
        self.assertEqual(result, 1)

    def test_nbr(self):
        query = 10
        export_1 = Export()
        export_2 = Export({Path(Slot("nbr", 0)): 20})
        export_3 = Export({Path(Slot("nbr", 0)): 30})
        self.vm.reset(ContextMock(1, {1: export_1, 2: export_2, 3: export_3}))
        result = self.field_calculus.nbr(query)
        self.assertIsInstance(result, Field)
        self.assertEqual(result.data, {1: 10, 2: 20, 3: 30})
        result2 = self.field_calculus.nbr(query)
        ## it has a different path
        self.assertEqual(result2.data, {1: 10})

    def test_branch_true(self):
        condition = MagicMock(return_value=True)
        then = MagicMock(return_value="then_result")
        orElse = MagicMock()
        result = self.field_calculus.branch(condition, then, orElse)
        condition.assert_called_once()
        then.assert_called_once()
        orElse.assert_not_called()
        self.assertEqual(result, "then_result")

    def test_branch_false(self):
        condition = MagicMock(return_value=False)
        then = MagicMock()
        orElse = MagicMock(return_value="else_result")
        result = self.field_calculus.branch(condition, then, orElse)
        condition.assert_called_once()
        then.assert_not_called()
        orElse.assert_called_once()
        self.assertEqual(result, "else_result")

    def test_branch_alignment(self):
        export_1 = Export()
        path_2 = Path(Slot("branch-True", 0)).push(Slot("nbr", 0))
        path_3 = Path(Slot("branch-False", 0)).push(Slot("nbr", 0))
        export_2 = Export({path_2: 20})
        export_3 = Export({path_3: 30})
        self.vm.reset(ContextMock(1, {1: export_1, 2: export_2, 3: export_3}))
        result = self.field_calculus.branch(lambda: True, lambda: self.field_calculus.nbr(10), lambda: self.field_calculus.nbr(20))
        self.assertEqual(result.data, {2: 20, 1: 10})

if __name__ == '__main__':
    unittest.main()