import unittest
from core import Export
from core import Path

class ExportTestCase(unittest.TestCase):
    def setUp(self):
        self.export = Export()

    def test_put_and_get(self):
        self.export.put("path1", "value1")
        self.export.put("path2", "value2")
        self.assertEqual(self.export.get("path1"), "value1")
        self.assertEqual(self.export.get("path2"), "value2")

    def test_get_nonexistent_path(self):
        self.assertIsNone(self.export.get("nonexistent_path"))

    def test_root(self):
        self.export.put(Path(), "root_value")
        self.assertEqual(self.export.root(), "root_value")

    def test_paths(self):
        self.export.put("path1", "value1")
        self.export.put("path2", "value2")
        self.assertEqual(self.export.paths, {"path1": "value1", "path2": "value2"})

    def test_equality(self):
        export1 = Export({"path1": "value1", "path2": "value2"})
        export2 = Export({"path1": "value1", "path2": "value2"})
        export3 = Export({"path1": "value1", "path3": "value3"})
        self.assertEqual(export1, export2)
        self.assertNotEqual(export1, export3)

    def test_hash(self):
        export1 = Export({"path1": "value1", "path2": "value2"})
        export2 = Export({"path1": "value1", "path2": "value2"})
        self.assertEqual(hash(export1), hash(export2))

    def test_string_representation(self):
        self.export.put("path1", "value1")
        self.export.put("path2", "value2")
        self.assertEqual(str(self.export), "{'path1': 'value1', 'path2': 'value2'}")

if __name__ == '__main__':
    unittest.main()