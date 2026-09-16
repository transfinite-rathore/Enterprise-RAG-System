import re
from .correction_strategy import QueryCorrectionRule
from ....model.user_query import UserQuery



class RemoveRepeatedPunctuationRule(QueryCorrectionRule):

    def correct(self, query: UserQuery) -> UserQuery:
        query.query = re.sub(r"([?!.,])\1+", r"\1", query.query)
        return query