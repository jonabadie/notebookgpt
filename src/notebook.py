import json

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

DEFAULT_FORMAT = {
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.9"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
 }

class Notebook():
    def __init__(self, filename="notebook.ipynb"):
        self.filename = filename
        self.cells = []

    def create_markdown(self, text):
        cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": text
        }
        self.cells.append(cell)
    
    def create_code(self, text):
        cell = {
            "cell_type": "code",
            "id": "b3c3d3e0",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": text
        }
        self.cells.append(cell)
    
    def _format_json(self):
        return {"cells": self.cells, **DEFAULT_FORMAT}
    
    def save_file(self):
        with open(self.filename, 'w') as f:
            json_data = self._format_json()
            json.dump(json_data, f)

    def _get_last_cell_output(self, nb):
        last_output = nb.cells[-1].outputs[0]
        data = last_output.get("data")
        last_cell_output = data["text/plain"] if data else last_output.text
        return last_cell_output

    def execute_notebook(self):
        with open(self.filename) as f:
            nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='dsr-b35')
        ep.preprocess(nb, {'metadata': {'path': './'}})
        with open(self.filename, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        last_cell_output = self._get_last_cell_output(nb)
        return last_cell_output
