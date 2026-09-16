from qdrant_client import AsyncQdrantClient,QdrantClient
from .QdrantVectorStore import QdrantVectorStore
from .AsyncQdrantVectorStore import AsyncQdrantVectorStore

class VSFactory:
    
    def __init__(self,client):
        self.client=client
    
    def create_vector_store(self):
        if isinstance(self.client,AsyncQdrantClient):
            return AsyncQdrantVectorStore(self.client)
        
        if isinstance(self.client,QdrantClient):
            return QdrantVectorStore(self.client)
        
    def close(self):
        self.client.close()