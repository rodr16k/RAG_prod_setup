# app/rag/qdrant_utils.py
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")


def get_qdrant_client() -> QdrantClient:
    """Initialize and return Qdrant client"""
    return QdrantClient(url=QDRANT_URL,
                        api_key=QDRANT_API_KEY or None,
                        check_compatibility=False)


def create_collection(client: QdrantClient, collection_name: str, vector_size: int = 1536):
    """Create a collection if it doesn't exist"""
    try:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size, distance=Distance.COSINE),
        )
        return True
    except Exception as e:
        print(f"Collection creation failed (may already exist): {e}")
        return False
