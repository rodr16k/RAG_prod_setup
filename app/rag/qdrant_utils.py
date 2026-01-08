# app/rag/qdrant_utils.py
import os
from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams,
    PointStruct, Filter,
    FieldCondition, MatchValue)
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")


def get_qdrant_client() -> QdrantClient:
    """Initialize and return Qdrant client"""
    return QdrantClient(url=QDRANT_URL,
                        api_key=QDRANT_API_KEY or None,
                        check_compatibility=False)


def create_collection(client: QdrantClient,
                      collection_name: str,
                      vector_size: int = 1536) -> bool:
    """Create a collection if it doesn't exist"""
    try:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size, distance=Distance.COSINE),
        )
        return True
    except Exception as e:
        if "already exist" in str(e):
            print(f"Collection {collection_name} already exists")
            return True
        print(f"Collection creation failed: {e}")
        return False


def upsert_docs(client: QdrantClient,
                collection_name: str,
                texts: List[str],
                embeddings: List[List[float]],
                metadata: List[dict],
                batch_size: int = 100
                ) -> None:
    """Upload documents to Wdrant in batches"""
    points = []
    for idx, (text, embedding, meta) in enumerate(zip(texts,
                                                      embeddings,
                                                      metadata)):
        points.append(
            PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "text": text,
                    "metadata": meta
                }
            )
        )

    for i in range(0, len(points), batch_size):
        batch = points[i: i + batch_size]
        client.upsert(collection_name=collection_name,
                      points=batch)

    print(f"{len(points)} documents uploaded to collection '{collection_name}'")


def search_similar(
        client: QdrantClient,
        collection_name: str,
        query_embedding: List[float],
        limit: int = 5
) -> List[dict]:
    """Search for similar documents"""
    results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=limit,
        with_payload=True
    )
    return [
        {
            "text": result.payload["text"],
            "metadata": result.payload["metadata"],
            "score": result.score
        }
        for result in results
    ]
