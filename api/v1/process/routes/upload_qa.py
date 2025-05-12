import os
import shutil

from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional, List
from pydantic import BaseModel
from tempfile import NamedTemporaryFile

from services.file.embedding_pipeline import embedding_pipeline
from models.file.qa_input import QARequest
from core.constants import EMBEDDING_MODEL_NAME, STORAGE_PATH

process_router = APIRouter(prefix="")

@process_router.post("/qa")
async def process_qa_list(input: QARequest):
    same_vectorstore = False
    combined_text = "\n\n".join(
        [f"Question: {qa.question}\nAnswer: {qa.answer}" for qa in input.qa_list]
    )

    vector_store_path = os.path.join(STORAGE_PATH, f"vectorstores/{input.file_name}")
    if os.path.exists(vector_store_path):
        same_vectorstore = True

    embedding_pipeline(EMBEDDING_MODEL_NAME, combined_text.lower(), vector_store_path, same_vectorstore)
    return {"processedText": f"Processed {len(input.qa_list)} Q&A pairs"}
