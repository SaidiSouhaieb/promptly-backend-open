from typing import List
from pydantic import BaseModel

from models.file.qa_input import QAItem


class UploadResponse(BaseModel):
    message: str
    chatbot_id: int
    file_name: str


class UploadQAResponse(UploadResponse):
    qa_list: List[QAItem]


class UploadTextResponse(UploadResponse):
    text: str
