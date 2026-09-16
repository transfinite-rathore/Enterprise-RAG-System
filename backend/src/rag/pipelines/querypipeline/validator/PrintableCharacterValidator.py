from ....model.user_query import UserQuery
from .validation_strategy import QueryValidatorRule


class PrintableCharacterValidator(QueryValidatorRule):
    
    def validate_query(self, query: UserQuery) -> bool:
        if not query.query.isprintable():
            return False
        return True
