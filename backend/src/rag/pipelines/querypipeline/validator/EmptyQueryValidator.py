from ....model.user_query import UserQuery
from .validation_strategy import QueryValidatorRule


class EmptyQueryValidator(QueryValidatorRule):
    
    def validate_query(self, user_query: UserQuery) -> bool:
        query=user_query.query
        
        if not query.strip() :
            return False
        return True