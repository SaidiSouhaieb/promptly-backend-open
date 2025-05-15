import os


def get_file_type(filename: str) -> str:
    """
    Returns the extension of the given filename (including the dot).

    Parameters:
        filename (str): The full filename.

    Returns:
        str: The file extension (e.g., '.txt')
    """
    _, ext = os.path.splitext(filename)
    return ext.replace(".", "")
