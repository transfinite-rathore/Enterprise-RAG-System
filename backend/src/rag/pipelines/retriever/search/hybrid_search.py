from ....model.retrieved_document import RetrievedDocument
from ....model.query_context import QueryContext
from .search_strategy import SearchingRule
from ....factories.vectorstore.VectorStore import VectorStoreInterface
from typing import List

class HybridSearchRule(SearchingRule):
  
    def search(self, client: VectorStoreInterface, collection_name: str,query_context:QueryContext , top_k: int = 50) -> List[RetrievedDocument]:
  
        return client.similarity_hybrid_search(collection_name,query_context.dense_embedding,query_context.sparse_embedding,top_k)

