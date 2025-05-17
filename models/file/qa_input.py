from typing import List
from pydantic import BaseModel


class QAItem(BaseModel):
    question: str
    answer: str


class QARequest(BaseModel):
    qa_list: List[QAItem]
    file_name: str
    chatbot_id: int
