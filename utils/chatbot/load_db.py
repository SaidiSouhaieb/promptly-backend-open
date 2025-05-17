from langchain_community.vectorstores import Chroma
from chromadb.config import Settings as ChromaSettings

from utils.chatbot.load_embeddings import load_hugging_face_embeddings


def load_db(embedding_model_name, db_path, device="cpu"):
    embedding_model = load_hugging_face_embeddings(embedding_model_name, device)

    chroma_settings = ChromaSettings(anonymized_telemetry=False, is_persistent=True)
    db = Chroma(
        persist_directory=db_path,
        embedding_function=embedding_model,
        client_settings=chroma_settings,
        collection_name="example_collection",
    )
    return db
