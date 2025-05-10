from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker


def get_semantic_chunking(text, embeddings):
    """Split text into semantically meaningful chunks using sentence and paragraph boundaries.

    Args:
        text: The text content to split into chunks

    Returns:
        List of Document objects containing the chunks
    """
    text_splitter = SemanticChunker(embeddings)
    return text_splitter.create_documents([text])
