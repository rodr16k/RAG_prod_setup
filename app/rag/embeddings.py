import os
from typing import List
from dotenv import load_dotenv
import asyncio

load_dotenv()


def get_embedding_model():
    """Initialize and return embedding model"""
    provider = os.getenv("EMBEDDING_PROVIDER", "openai").lower()

    if provider == 'openai':
        return _get_openai_embeddings()
    elif provider == 'huggingface':
        return _get_huggingface_embeddings()
    else:
        raise ValueError(
            f"Unsupported EMBEDDING_PROVIDER: {provider}. Use 'openai' or 'huggingface'")


def _get_openai_embeddings():
    """Initialize OpenAI embeddings"""
    from langchain_openai import OpenAIEmbeddings

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env")

    return OpenAIEmbeddings(
        openai_api_key=api_key,
        model=os.getenv("OPENAI_MODEL", "text-embedding-ada-002")
    )


def _get_huggingface_embeddings():
    """Initialize HuggingFace embeddings"""
    from langchain_huggingface import HuggingFaceEmbeddings

    model_name = os.getenv("HUGGINGFACE_MODEL",
                           "sentence-transformers/all-MiniLM-L6-v2")

    print(
        f"Loading HuggingFace model: {model_name} (this may take a while on first run)")

    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},  # Change to 'cuda' if GPU is available
        encode_kwargs={'normalize_embeddings': True}
    )


async def generate_embeddings_async(texts: List[str]) -> List[List[float]]:
    """Asynchronous embedding generation"""
    embedding_model = get_embedding_model()

    # Use asynch if available
    if hasattr(embedding_model, 'aembed_documents'):
        return await embedding_model.aembed_documents(texts)
    else:
        import concurrent.futures
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor as pool:
            return await loop.run_in_executor(pool, embedding_model.embed_documents, texts)


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate embeddings (synch wrap for asynch function)"""
    return asyncio.run(generate_embeddings_async(texts))
