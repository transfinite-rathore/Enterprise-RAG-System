
from typing import List,Dict
from ....model.user_query import UserQuery
from .correction_strategy import QueryCorrectionRule

class QueryCorrecter:
    
    def __init__(self,rules:List[QueryCorrectionRule]) -> None:
        self.correction_rules=rules
        
    def correct(self,user_query:UserQuery) -> Dict:
        query=user_query.model_copy()
        for rule in self.correction_rules:
            query=rule.correct(query)
            
        return {"originial_query":user_query,
                "corrected_query":query}