import json
from pydantic import BaseModel, model_validator


class FileInput(BaseModel):
    file_name: str
    chatbot_id: int

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
