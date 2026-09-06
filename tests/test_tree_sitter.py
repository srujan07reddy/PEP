import unittest
import sys
import os

# Add the project root to the path so we can import core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from registry.adapters.tree_sitter_adapter import TreeSitterAdapter

class TestTreeSitterAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = TreeSitterAdapter()
        self.source_code = """
import os
from sys import path

class Base:
    pass

class MyClass(Base):
    def my_method(self):
        os.path.join("a", "b")
        self.other_method()

def standalone_func():
    MyClass()
"""
        self.ast = self.adapter.parse(self.source_code, "python")

    def test_extract_classes(self):
        classes = self.adapter.extract_classes(self.ast)
        class_names = [c["name"] for c in classes]
        self.assertIn("MyClass", class_names)
        self.assertIn("Base", class_names)

    def test_extract_functions(self):
        functions = self.adapter.extract_functions(self.ast)
        function_names = [f["name"] for f in functions]
        self.assertIn("my_method", function_names)
        self.assertIn("standalone_func", function_names)

    def test_extract_inheritance(self):
        inheritance = self.adapter.extract_inheritance(self.ast)
        my_class_inh = next((i for i in inheritance if i["class"] == "MyClass"), None)
        self.assertIsNotNone(my_class_inh)
        self.assertIn("Base", my_class_inh["inherits_from"])

    def test_extract_imports(self):
        imports = self.adapter.extract_imports(self.ast)
        import_modules = [i["module"] for i in imports]
        self.assertTrue(any("import os" in m for m in import_modules))

    def test_extract_call_graph(self):
        calls = self.adapter.extract_call_graph(self.ast)
        self.assertTrue(any(c["caller"] == "my_method" and c["callee"] == "other_method" for c in calls))
        self.assertTrue(any(c["caller"] == "standalone_func" and c["callee"] == "MyClass" for c in calls))

if __name__ == "__main__":
    unittest.main()
