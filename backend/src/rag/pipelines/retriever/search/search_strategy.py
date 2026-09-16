from abc import ABC, abstractmethod
from typing import Iterable,List,Optional,Dict
from ....model.retrieved_document import RetrievedDocument
from ....model.query_context import QueryContext
from ....factories.vectorstore.VectorStore import VectorStoreInterface

class SearchingRule(ABC):
    @abstractmethod
    def search(self,client:VectorStoreInterface,collection_name:str,query_context:QueryContext,
               top_k:int=50) -> List[RetrievedDocument]:
        pass