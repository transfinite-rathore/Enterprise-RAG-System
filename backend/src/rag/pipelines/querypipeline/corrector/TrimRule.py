from .correction_strategy import QueryCorrectionRule
from ....model.user_query import UserQuery

class TrimWhitespaceRule(QueryCorrectionRule):

    def correct(self, query: UserQuery) -> UserQuery:
        query.query = query.query.strip()
        return query