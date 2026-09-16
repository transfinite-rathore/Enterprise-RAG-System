import re
from .correction_strategy import QueryCorrectionRule
from ....model.user_query import UserQuery

class CollapseSpacesRule(QueryCorrectionRule):

    def correct(self, query: UserQuery) -> UserQuery:
        query.query = re.sub(r"\s+", " ", query.query)
        return query