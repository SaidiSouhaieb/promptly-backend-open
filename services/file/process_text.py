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
    """Processes text content into a Chroma vector store.

    Args:
        raw_text: The text content to process
        embedding_model_name: Name of the HuggingFace embeddings model to use
        chunk_size: Not used for semantic chunking, kept for API compatibility

    Returns:
        Chroma vector store containing the embedded documents
    """

    document_db_path = os.path.join(db_path, "semantic")
    embeddings = load_hugging_face_embeddings(embedding_model_name)
    semantic_documents = get_semantic_chunking(raw_text, embeddings)

    if same_vectorstore:
        client = chromadb.Client(
            ChromaSettings(
                anonymized_telemetry=False,
                is_persistent=True,
                persist_directory=document_db_path,
            )
        )
        coll = client.get_collection("example_collection")
        old_documents = coll.get(include=["documents"])
        old_documents_docs = old_documents["documents"]
        old_documents_ids = old_documents["ids"]

        ids = [str(uuid.uuid4()) for _ in range(len(semantic_documents))]
        documents_docs = [doc.page_content for doc in semantic_documents]

        documents = old_documents_docs + documents_docs
        ids = old_documents_ids + ids
        db = Chroma.from_texts(
            texts=documents,
            ids=ids,
            collection_name="example_collection",
            embedding=embeddings,
            persist_directory=document_db_path,
            client_settings=ChromaSettings(
                anonymized_telemetry=CHROMA_CLIENT_SETTINGS["anonymized_telemetry"],
                is_persistent=CHROMA_CLIENT_SETTINGS["is_persistent"],
            ),
        )
        db.persist()
        return db

    else:
        db = Chroma.from_documents(
            documents=semantic_documents,
            collection_name="example_collection",
            embedding=embeddings,
            persist_directory=document_db_path,
            client_settings=ChromaSettings(
                anonymized_telemetry=CHROMA_CLIENT_SETTINGS["anonymized_telemetry"],
                is_persistent=CHROMA_CLIENT_SETTINGS["is_persistent"],
            ),
        )
        db.persist()
        return db
