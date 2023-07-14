import unittest
import json
import os
from notebook import Notebook
import nbformat


class TestNotebook(unittest.TestCase):
    def setUp(self):
        self.notebook = Notebook("testing_notebook.ipynb")

    def test_create_markdown(self):
        self.notebook.create_markdown("# Test")
        self.assertEqual(len(self.notebook.cells), 1)
        self.assertEqual(self.notebook.cells[0]["cell_type"], "markdown")
        self.assertEqual(self.notebook.cells[0]["source"], "# Test")

    def test_create_code(self):
        self.notebook.create_code("print('Hello, world!')")
        self.assertEqual(len(self.notebook.cells), 1)
        self.assertEqual(self.notebook.cells[0]["cell_type"], "code")
        self.assertEqual(self.notebook.cells[0]["source"], "print('Hello, world!')")

    def test_save_file(self):
        self.notebook.create_markdown("# Test")
        self.notebook.create_code("print('Hello, world!')")
        self.notebook.save_file()
        with open(self.notebook.filename, "r") as f:
            json_data = json.load(f)
            self.assertEqual(len(json_data["cells"]), 2)
            self.assertEqual(json_data["cells"][0]["cell_type"], "markdown")
            self.assertEqual(json_data["cells"][0]["source"], "# Test")
            self.assertEqual(json_data["cells"][1]["cell_type"], "code")
            self.assertEqual(json_data["cells"][1]["source"], "print('Hello, world!')")

    def test_create_multiple_markdown_and_code(self):
        self.notebook.create_markdown("# Test 1")
        self.notebook.create_code("print('Hello, world!')")
        self.notebook.create_markdown("# Test 2")
        self.notebook.create_code("print('Goodbye, world!')")
        self.assertEqual(len(self.notebook.cells), 4)
        self.assertEqual(self.notebook.cells[0]["cell_type"], "markdown")
        self.assertEqual(self.notebook.cells[0]["source"], "# Test 1")
        self.assertEqual(self.notebook.cells[1]["cell_type"], "code")
        self.assertEqual(self.notebook.cells[1]["source"], "print('Hello, world!')")
        self.assertEqual(self.notebook.cells[2]["cell_type"], "markdown")
        self.assertEqual(self.notebook.cells[2]["source"], "# Test 2")
        self.assertEqual(self.notebook.cells[3]["cell_type"], "code")
        self.assertEqual(self.notebook.cells[3]["source"], "print('Goodbye, world!')")

    def test_execute_notebook_file(self):
        self.notebook.create_code("a = 1\nb = 2\na + b")
        self.notebook.save_file()
        self.notebook.execute_notebook()
        with open(self.notebook.filename) as f:
            nb = nbformat.read(f, as_version=4)
            cell = nb["cells"][0]
            self.assertEqual(cell["outputs"][0]["data"]["text/plain"], "3")

    def test_execute_notebook_file_multiple_cells(self):
        self.notebook.create_code("a = 1\nb = 2\na + b")
        self.notebook.create_code("c = 10\nd = 4\nc + b / (a + b)")
        self.notebook.save_file()
        self.notebook.execute_notebook()
        with open(self.notebook.filename) as f:
            nb = nbformat.read(f, as_version=4)
            cell = nb["cells"][0]
            self.assertEqual(cell["outputs"][0]["data"]["text/plain"], "3")

    def test_execute_notebook_return_value(self):
        self.notebook.create_code("a = 1\nb = 2\na + b")
        self.notebook.save_file()
        last_cell_output = self.notebook.execute_notebook()
        self.assertEqual(last_cell_output, "3")

    def tearDown(self):
        if os.path.exists(self.notebook.filename):
            os.remove(self.notebook.filename)


if __name__ == "__main__":
    unittest.main()
