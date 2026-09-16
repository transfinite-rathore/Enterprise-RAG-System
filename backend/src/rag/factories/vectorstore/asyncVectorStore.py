from abc import ABC, abstractmethod
from typing import Iterable, Any, Optional, Union, List, Dict
import numpy as np
from numpy.typing import NDArray
from langchain_core.documents import Document

from ...model.retrieved_document import RetrievedDocument

# =========================================================================
# 1. Asynchronous Interface (For FastAPI, async workers, ingestion)
# =========================================================================
class AsyncVectorStoreInterface(ABC):
    

    @abstractmethod
    async def create_collection(self) -> None:
        """Asynchronously create a new vector database collection."""
        pass
    
    @abstractmethod
    async def save_documents(
        self,
        dense_embeddings: Iterable,
        sparse_embeddings: Iterable,
        collection_name: str,
        chunks: Iterable[Document]
    ) -> Any:
        """Asynchronously save chunks and their embeddings to the vector store."""
        pass

    @abstractmethod
    async def similarity_dense_search(
        self,
        collection_name: str,
        query_embedding: Union[NDArray[np.float32], List[float], Iterable[float]],
        limit: int = 25
    ) -> List[RetrievedDocument]:
        """Asynchronously search the vector store using dense retrieval."""
        pass

    @abstractmethod
    async def similarity_sparse_search(
        self,
        collection_name: str,
        query_embedding: Dict[int, float],
        limit: int = 25
    ) -> List[RetrievedDocument]:
        """Asynchronously search the vector store using sparse retrieval."""
        pass
    
    @abstractmethod
    async def similarity_hybrid_search(
        self,
        collection_name: str,
        dense_query_embedding: Optional[Union[NDArray[np.float32], List[float], Iterable[float]]] = None,
        sparse_query_embedding: Optional[Dict[int, float]] = None,
        limit: int = 25
    ) -> List[RetrievedDocument]:
        """Asynchronously search the vector store using hybrid retrieval (RRF)."""
        pass
        
    @abstractmethod
    async def delete_document(self) -> None:
        """Asynchronously delete a document from the collection."""
        pass
    
    @abstractmethod
    async def collection_exists(self, collection_name: str) -> bool:
        """Asynchronously check if a collection exists."""
        pass
    
    @abstractmethod
    async def close(self):
        pass

# =========================================================================
# 2. Synchronous Interface (For CLI, standard RAG Orchestrator)
# =========================================================================
# class SyncVectorStoreInterface(ABC):
    
#     @abstractmethod
#     def create_collection(self) -> None:
#         """Synchronously create a new vector database collection."""
#         pass
    
#     @abstractmethod
#     def save_documents(
#         self,
#         dense_embeddings: Iterable,
#         sparse_embeddings: Iterable,
#         collection_name: str,
#         chunks: Iterable[Document]
#     ) -> Any:
#         """Synchronously save chunks and their embeddings to the vector store."""
#         pass

#     @abstractmethod
#     def similarity_dense_search(
#         self,
#         collection_name: str,
#         query_embedding: Union[NDArray[np.float32], List[float], Iterable[float]],
#         limit: int = 25
#     ) -> List[RetrievedDocument]:
#         """Synchronously search the vector store using dense retrieval."""
#         pass

#     @abstractmethod
#     def similarity_sparse_search(
#         self,
#         collection_name: str,
#         query_embedding: Dict[int, float],
#         limit: int = 25
#     ) -> List[RetrievedDocument]:
#         """Synchronously search the vector store using sparse retrieval."""
#         pass
    
#     @abstractmethod
#     def similarity_hybrid_search(
#         self,
#         collection_name: str,
#         dense_query_embedding: Optional[Union[NDArray[np.float32], List[float], Iterable[float]]] = None,
#         sparse_query_embedding: Optional[Dict[int, float]] = None,
#         limit: int = 25
#     ) -> List[RetrievedDocument]:
#         """Synchronously search the vector store using hybrid retrieval (RRF)."""
#         pass
        
#     @abstractmethod
#     def delete_document(self) -> None:
#         """Synchronously delete a document from the collection."""
#         pass
    
#     @abstractmethod
#     def collection_exists(self, collection_name: str) -> bool:
#         """Synchronously check if a collection exists."""
#         pass