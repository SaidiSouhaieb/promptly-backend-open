from pydantic import BaseModel, root_validator, ValidationError
from typing import List


class TextInput(BaseModel):
    text: str
    model_name: str

    @root_validator(pre=True)
    def validate_model_name(cls, values):
        available_models = ["llama3", "mistral7b"]
        model_name = values.get("model_name")

        if model_name not in available_models:
            raise ValueError(
                f"Invalid model name. Available models: {', '.join(available_models)}"
            )
        return values
