from typing import List
from ....model.user_query import UserQuery
from .validation_strategy import QueryValidatorRule

class QueryValidator:
    
    def __init__(self,validator_rules:List[QueryValidatorRule]) -> None:
        self.validator_rules=validator_rules
        
        
    def apply_validation(self,user_query:UserQuery):
        
        validation_result={}
        for rule in self.validator_rules:
            validation_result[type(rule).__name__]=rule.validate_query(user_query)
            
        return validation_result
        ...