import os
from core.constants import STORAGE_PATH


def get_semantic_folder_path(file_name: str) -> str:
    return os.path.join(STORAGE_PATH, "vectorstores", file_name, "semantic")
