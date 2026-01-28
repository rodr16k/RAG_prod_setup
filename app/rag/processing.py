import hashlib
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter


def calculate_hash(content: str) -> str:
    """Calculate SHA256 hash of content"""
    return hashlib.sha256(content.encode()).hexdigest()


def split_documents(
        texts: List[str],
        chunk_size: int = 500,
        chunk_overlap: int = 50,
) -> List[str]:
    """Split documents into chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_overlap=chunk_overlap,
        chunk_size=chunk_size,
        length_function=len
    )

    all_chunks = []
    for text in texts:
        chunks = splitter.split_text(text)
        all_chunks.extend(chunks)

    return all_chunks


def load_text_file(file_path: str) -> str:
    """Load content from a text file"""
    with open(file_path, "r", encoding='utf-8') as f:
        return f.read()
