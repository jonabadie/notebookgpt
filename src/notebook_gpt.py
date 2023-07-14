import sys

from notebook_chain import NotebookChain
from utilities import file_exists

if __name__ == "__main__":
    filename = "data/titanic_train.csv"
    steps = 10
    if sys.argv[1:]:
        filename = sys.argv[1]
        if not file_exists(filename):
            print(f"File {filename} does not exist.")
            sys.exit(1)
    if sys.argv[2:]:
        steps = int(sys.argv[2])

    notebook_chain = NotebookChain(filename, steps=steps)
    notebook_chain.run()