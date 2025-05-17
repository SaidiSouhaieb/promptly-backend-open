import os
import shutil

from fastapi import UploadFile
from tempfile import NamedTemporaryFile

from core.constants import STORAGE_PATH


def create_temp_file(upload_file: UploadFile):
    with NamedTemporaryFile(delete=False, suffix=upload_file.filename) as tmp:
        temp_path = os.path.join(STORAGE_PATH, tmp.name)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

    return temp_path
