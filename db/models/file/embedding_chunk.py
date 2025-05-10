from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, text

from db.base import BaseModel


class EmbeddingChunk(BaseModel):
    __tablename__ = "embedding_chunks"

    id = Column(Integer, primary_key=True, nullable=False)
    data_souce_id = Column(Integer, ForeignKey("DataSource.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    embedding = Column(String, nullable=False)
