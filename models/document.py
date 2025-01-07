from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from uuid import uuid4
from .base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chunks = relationship(
        "DocumentChunk", back_populates="document", cascade="all, delete-orphan"
    )
    user = relationship("User", back_populates="documents")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID, primary_key=True, default=uuid4)
    document_id = Column(UUID, ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    embedding = Column(Vector(1536))
    contextualized_content = Column(Text)
    labels = Column(JSONB, default={})
    chunk_metadata = Column(JSONB, default={})
    document = relationship("Document", back_populates="chunks")
