from .metric import BaseRankingMetric
from ....model.evaluation_context import EvaluatorContext
from typing import List
from itertools import islice

class HitRate(BaseRankingMetric):
    
    def __init__(self,k:int=5) -> None:
        self.k=k
    
    @property
    def name(self):
        return f"hit_rate@{self.k}"
    ## Hit rate works on document id not its content
    def calculate(self,chunk_ids:List[str],context:EvaluatorContext) -> float:
        for id in chunk_ids[:self.k]:
            if id in context.relevant_ids:
                return 1.0
        return 0.0