import os

from llms.loaders.model_loader import ModelLoader

from utils.chatbot.load_db import load_db
from utils.chatbot.load_qa_chain import RetrievalQAChain
from llms.prompts.load_prompt import load_prompt

model_loader = ModelLoader()


def get_chain(db_path, embedding_model_name, model_name, text):
    llm = model_loader.load_model(model_name)
    prompt = load_prompt(model_name)
    db = load_db(embedding_model_name, db_path)

    qa_chain = RetrievalQAChain(llm, prompt, db, text)
    return qa_chain
