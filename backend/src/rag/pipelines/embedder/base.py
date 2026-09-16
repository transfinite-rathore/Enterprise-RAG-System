from abc import ABC,abstractmethod
from langchain_core.documents import Document
from typing import Iterable,Optional

class BaseEmbedderProvider(ABC):
    @abstractmethod
    def embed_document(self,chunks:Iterable[Document])-> Iterable[float]:
        pass
    
    @abstractmethod
    def embed_query(self,query:str) -> Iterable[float]:
        pass