from abc import ABC, abstractmethod
from ....model.user_query import UserQuery

class QueryValidatorRule(ABC):
    @abstractmethod
    def validate_query(self,query:UserQuery) -> bool:
        pass