import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional, List
from pydantic import BaseModel
from tempfile import NamedTemporaryFile

from models.file.file_input import FileInput
from services.file.embedding_pipeline import embedding_pipeline
from services.file.content_extractor import ExtractContent
from utils.file.remove_file_extensions import remove_file_extension
from core.constants import EMBEDDING_MODEL_NAME, STORAGE_PATH

process_router = APIRouter(prefix="")
content_extractor = ExtractContent()


@process_router.post("/upload-file")
async def process_file_upload(
    file_name: str = Form(...),
    upload_file: UploadFile = File(...),
):
    same_vectorstore = False
    with NamedTemporaryFile(delete=False, suffix=upload_file.filename) as tmp:
        temp_path = os.path.join(STORAGE_PATH, tmp.name)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

    try:
        raw_text = content_extractor.get_text_content(temp_path)

        file_name = remove_file_extension(file_name)
        vector_store_path = os.path.join(STORAGE_PATH, f"vectorstores/{file_name}")
        if os.path.exists(vector_store_path):
            same_vectorstore = True

        embedding_pipeline(EMBEDDING_MODEL_NAME, raw_text.lower(), vector_store_path, same_vectorstore  )
        return {"processedText": f"Processed: {raw_text[:200]}..."}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
