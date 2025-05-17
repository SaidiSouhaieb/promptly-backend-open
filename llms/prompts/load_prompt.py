from langchain import PromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

from llms.prompts.templates.llama import LLAMA_CUSTOM_TEMPLATE
from llms.prompts.templates.mistral import MISTRAL_CUSTOM_TEMPLATE

PROMPT_TEMPLATES = {
    "mistral7b": MISTRAL_CUSTOM_TEMPLATE,
    "llama3": LLAMA_CUSTOM_TEMPLATE,
}


def load_prompt(model_name):
    prompt_template = PROMPT_TEMPLATES.get(model_name)

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"],
    )
    return prompt
