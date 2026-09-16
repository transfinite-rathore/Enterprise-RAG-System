from ....model.retrieved_document import RetrievedDocument
from ....model.query_context import QueryContext
from .search_strategy import SearchingRule
from ....factories.vectorstore.VectorStore import VectorStoreInterface
from typing import Dict, Iterable, List

class DenseSearchRule(SearchingRule):
  
    def search(self, client: VectorStoreInterface, collection_name: str, query_context:QueryContext, top_k: int = 50) -> List[RetrievedDocument]:

        return client.similarity_dense_search(collection_name,query_context.dense_embedding,top_k)
        
        
    # def search(self,vector_store:VectorStoreInterface,query:Iterable[float],collection_name:str,top_k:int):
    #     return vector_store.similarity_search(query,collection_name,top_k)

