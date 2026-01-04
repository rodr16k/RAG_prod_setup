from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content_hash = Column(String, unique=True, index=True)
    file_path = Column(String)
    upload_date = Column(DateTime, default=func.now())
    metadata_ = Column("metedata", JSON)


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    source_documents = Column(JSON)
