from abc import ABC,abstractmethod
from typing import Iterable
from ....model.query_context import QueryContext
from ....model.reranked_context import RerankContext
from ....model.retrieved_document import RetrievedDocument


class RerankerStrategy(ABC):
    
    @abstractmethod
    def rerank(self,query:QueryContext,reterived_documents:Iterable[RetrievedDocument],top_k:int) -> Iterable[RerankContext]:
        pass