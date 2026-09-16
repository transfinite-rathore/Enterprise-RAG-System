from typing import List
from .search.search_strategy import SearchingRule
from ...model.query_context import QueryContext
from ...model.retrieved_document import RetrievedDocument

class Retriever:
    
    def __init__(self,vs,searching_rule:SearchingRule,collection_name:str,top_k:int=10) -> None:
        self.vector_store=vs
        self.searching_rule=searching_rule
        self.top_k = top_k
        self.collection_name=collection_name
        
            
    def retrieve(self,query:QueryContext) -> List[RetrievedDocument]:
        # if query.embedding is None:
        #     raise ValueError("Query embedding is required for retrieval")
        
        if not self.vector_store.collection_exist(self.collection_name):
            raise Exception("Can not find Collection in Vector DB")
        
        results=self.searching_rule.search(self.vector_store,self.collection_name,query,self.top_k)
        
        return results
