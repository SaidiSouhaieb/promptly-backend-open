import os

from services.file.process_text import process_txt


def embedding_pipeline(
    embedding_model,
    raw_text,
    vector_store_path,
    same_vectorstore=False,
    chunk_size=1000,
):
    os.makedirs(vector_store_path, exist_ok=True)

    vector_store = process_txt(
        raw_text=raw_text,
        embedding_model_name=embedding_model,
        chunk_size=chunk_size,
        db_path=vector_store_path,
        same_vectorstore=same_vectorstore,
    )

    vector_store.persist()
    print(f"Processing complete. Vector store saved to '{vector_store_path}'.")
