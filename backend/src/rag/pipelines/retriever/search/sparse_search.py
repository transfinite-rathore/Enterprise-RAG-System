from ....model.retrieved_document import RetrievedDocument
from .search_strategy import SearchingRule
from ....model.query_context import QueryContext
from ....factories.vectorstore.VectorStore import VectorStoreInterface
from typing import Dict, Iterable, List

class SparseSearchRule(SearchingRule):
  
    def search(self, client: VectorStoreInterface, collection_name: str, query_context:QueryContext, top_k: int = 50) -> List[RetrievedDocument]:
        return client.similarity_sparse_search(collection_name,query_context.sparse_embedding,top_k)