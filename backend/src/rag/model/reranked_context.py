from .retrieved_document import RetrievedDocument


class RerankContext(RetrievedDocument):
    rerank_score:float
    rerank_rank:int