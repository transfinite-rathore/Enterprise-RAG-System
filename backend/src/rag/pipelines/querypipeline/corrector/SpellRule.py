from .correction_strategy import QueryCorrectionRule
from ....model.user_query import UserQuery

class SpellCorrectionRule(QueryCorrectionRule):

    def correct(self, query: UserQuery) -> UserQuery:
        # TODO:
        # Integrate SymSpell / pyspellchecker / LLM
        return query