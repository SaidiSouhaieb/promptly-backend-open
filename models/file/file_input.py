from pydantic import BaseModel


class FileInput(BaseModel):
    file_name: str
