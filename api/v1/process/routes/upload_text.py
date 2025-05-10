import os
import shutil

from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional, List
from pydantic import BaseModel
from tempfile import NamedTemporaryFile

from services.file.embedding_pipeline import embedding_pipeline
from services.file.content_extractor import ExtractContent
from models.file.text_input import ProcessInput
from core.constants import EMBEDDING_MODEL_NAME, STORAGE_PATH


process_router = APIRouter(prefix="")
content_extractor = ExtractContent()


@process_router.post("/text")
async def process_text_input(
    input: ProcessInput,
):
    same_vectorstore = False
    vector_store_path = os.path.join(STORAGE_PATH, f"vectorstores/{input.file_name}")

    if os.path.exists(vector_store_path):
        same_vectorstore = True

    embedding_pipeline(EMBEDDING_MODEL_NAME, input.text.lower(), vector_store_path, same_vectorstore)
    return {"processedText": f"Processed: {input.text[:200]}..."}
