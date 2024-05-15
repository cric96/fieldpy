import unittest
from core import Export
from core import Path
from core import Slot

class ExportTestCase(unittest.TestCase):
    def setUp(self):
        self.export = Export()

    def test_put_and_get(self):
        slot1 = Slot("slot1", 0)
        slot2 = Slot("slot2", 1)
        self.export.put(Path(slot1), "value1")
        self.export.put(Path(slot2), "value2")
        self.assertEqual(self.export.get(Path(slot1)), "value1")
        self.assertEqual(self.export.get(Path(slot2)), "value2")

    def test_get_nonexistent_path(self):
        non_existent_path = Path(Slot("nonexistent_slot", 999))
        self.assertIsNone(self.export.get(non_existent_path))

    def test_root(self):
        self.export.put(Path(), "root_value")
        self.assertEqual(self.export.root(), "root_value")

    def test_paths(self):
        path1 = Path(Slot("slot1", 0))
        path2 = Path(Slot("slot2", 1))
        self.export.put(path1, "value1")
        self.export.put(path2, "value2")
        self.assertEqual(self.export.paths, {path1: "value1", path2: "value2"})

    def test_equality(self):
        path1 = Path(Slot("slot1", 0))
        path2 = Path(Slot("slot2", 1))
        path3 = Path(Slot("slot3", 2))
        export1 = Export({path1: "value1", path2: "value2"})
        export2 = Export({path1: "value1", path2: "value2"})
        export3 = Export({path1: "value1", path3: "value3"})
        self.assertEqual(export1, export2)
        self.assertNotEqual(export1, export3)

    def test_hash(self):
        path1 = Path(Slot("slot1", 0))
        path2 = Path(Slot("slot2", 1))
        export1 = Export({path1: "value1", path2: "value2"})
        export2 = Export({path1: "value1", path2: "value2"})
        self.assertEqual(hash(export1), hash(export2))

    def test_string_representation(self):
        self.export.put(Path(Slot("path1", 0)), "value1")
        self.export.put(Path(Slot("path2", 1)), "value2")
        self.assertEqual(str(self.export), "{[('path1', 0)]: 'value1', [('path2', 1)]: 'value2'}")

if __name__ == '__main__':
    unittest.main()
