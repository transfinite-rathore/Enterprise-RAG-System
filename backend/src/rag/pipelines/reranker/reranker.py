from typing import Iterable,List
from .reranking_strategy.reranking_rule import RerankerStrategy
from ...model.query_context import QueryContext
from ...model.retrieved_document import RetrievedDocument
from ...model.reranked_context import RerankContext


class Reranker:
    def __init__(self,reranking_rule:RerankerStrategy,top_k:int=5) -> None:
        self.rerank_rule=reranking_rule
        self.top_k=top_k
        pass
    
    def rerank(self,query_context:QueryContext,documents:List[RetrievedDocument])-> Iterable[RerankContext]:
        reranked_result=self.rerank_rule.rerank(query_context,documents,self.top_k)
        return reranked_result