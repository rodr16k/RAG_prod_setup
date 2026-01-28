from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Document, ChatHistory
from typing import List, Optional


async def store_document(
        db: AsyncSession,
        filename: str,
        content_hash: str,
        file_path: str,
        metadata: dict
) -> Document:
    """Store document's metadata in PostgreSQL"""
    doc = Document(
        filename=filename,
        content_hash=content_hash,
        file_path=file_path,
        metadata=metadata
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc


async def get_document_by_hash(
        db: AsyncSession,
        content_hash: str
) -> Optional[Document]:
    """Check if document already exists"""
    result = await db.execute(
        select(Document).where(Document.content_hash == content_hash)
    )
    return result.scalar_one_or_none()


async def store_chat_history(
        db: AsyncSession,
        session_id: str,
        question: str,
        answer: str,
        source_documents: List[dict]
) -> ChatHistory:
    """Store chat interaction"""
    chat = ChatHistory(
        session_id=session_id,
        question=question,
        answer=answer,
        source_documents=source_documents
    )
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat
