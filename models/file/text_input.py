from pydantic import BaseModel


class ProcessInput(BaseModel):
    text: str = None
    file_name: str
    chatbot_id: int
