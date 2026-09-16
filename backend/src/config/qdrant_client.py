from qdrant_client import QdrantClient,AsyncQdrantClient
from dotenv import load_dotenv
import os


load_dotenv()


def create_qdrant_async_client() -> AsyncQdrantClient:
    client=AsyncQdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        cloud_inference=True,
        timeout=60
    )

    
    return client


def create_qdrant_client() -> QdrantClient:
    client=QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        cloud_inference=True
    )

    return client