from langchain_community.embeddings import HuggingFaceEmbeddings


def load_hugging_face_embeddings(embedding_model_name, device="cpu"):
    model_kwargs = {"device": device}
    encode_kwargs = {"normalize_embeddings": False}
    embedding_model = HuggingFaceEmbeddings(
        model_name=embedding_model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )

    return embedding_model
