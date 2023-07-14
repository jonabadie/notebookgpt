import os

def file_exists(filepath):
    """
    Checks if a file exists given its filepath.
    Returns True if the file exists, False otherwise.
    """
    return os.path.isfile(filepath)
