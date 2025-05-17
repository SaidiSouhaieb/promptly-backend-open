import os
import uuid
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from chromadb.config import Settings as ChromaSettings

from utils.file.semantic_chunking import get_semantic_chunking
from utils.chatbot.load_embeddings import load_hugging_face_embeddings
from core.constants import CHROMA_CLIENT_SETTINGS


def process_txt(
    raw_text: str,
    embedding_model_name: str,
    chunk_size: int = None,
    same_vectorstore: bool = False,
    db_path: str = None,
) -> Chroma:
    embeddings = load_hugging_face_embeddings(embedding_model_name)
    semantic_documents = get_semantic_chunking(raw_text, embeddings)

    client_settings = ChromaSettings(
        anonymized_telemetry=CHROMA_CLIENT_SETTINGS["anonymized_telemetry"],
        is_persistent=CHROMA_CLIENT_SETTINGS["is_persistent"],
        persist_directory=db_path,
    )

    texts = [doc.page_content for doc in semantic_documents]
    ids = [str(uuid.uuid4()) for _ in texts]

    if same_vectorstore:
        client = chromadb.Client(client_settings)
        try:
            coll = client.get_collection("example_collection")
            existing = coll.get(include=["documents"])
            texts = existing["documents"] + texts
            ids = existing["ids"] + ids
        except Exception as e:
            logging.warning(f"No existing vectorstore found, creating new one: {e}")
            return Chroma.from_texts(
                texts=texts,
                ids=ids,
                collection_name="example_collection",
                embedding=embeddings,
                persist_directory=db_path,
                client_settings=client_settings,
            )

        return Chroma.from_texts(
            texts=texts,
            ids=ids,
            collection_name="example_collection",
            embedding=embeddings,
            persist_directory=db_path,
            client_settings=client_settings,
        )

    return Chroma.from_documents(
        documents=semantic_documents,
        collection_name="example_collection",
        embedding=embeddings,
        persist_directory=db_path,
        client_settings=client_settings,
    )
