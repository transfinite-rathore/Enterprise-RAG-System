from abc import ABC,abstractmethod
from ....model.user_query import UserQuery
from ....model.query_context import QueryContext

class QueryRewriter(ABC):
    
    @abstractmethod
    def rewrite_query(self,query:UserQuery) -> QueryContext:
        
        pass