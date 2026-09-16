from typing import Iterable
from sentence_transformers import CrossEncoder
from ....model.query_context import QueryContext
# from backend.src.rag.model.query_context import QueryContext
from ....model.reranked_context import RerankContext
from ....model.retrieved_document import RetrievedDocument
from .reranking_rule import RerankerStrategy
from .....config.logging_config import set_logger

logger=set_logger(__name__,"logs/reterival.log")


class CrossEncoderReranker(RerankerStrategy):
    
    def __init__(self,model_path):
        self.model=CrossEncoder(model_path)
    
    def rerank(self, query: QueryContext, reterived_documents: Iterable[RetrievedDocument],top_k:int) -> Iterable[RerankContext]:
        
        
        processed_query=query.processed_query
        documents=list(reterived_documents)
        document_contents = [
            document.content
            for document in documents
        ]

        ranking_result = self.model.rank(
            processed_query,
            document_contents,
            top_k=top_k
        )

        return [
            RerankContext(
                **documents[result["corpus_id"]].model_dump(),
                rerank_rank=rank,
                rerank_score=result["score"]
            )
            for rank, result in enumerate(ranking_result, start=1)
        ]
        
        
