from typing import List

from ....model.evaluation_context import EvaluatorContext
from ....evaluation_pipeline.evaluation_metrics.ranking_metric.metric import BaseRankingMetric


class RecallAtK(BaseRankingMetric):
    
    def __init__(self,k:int=5) -> None:
        self.k=k
        
    @property
    def name(self):
        return f"Recall@{self.k}"
    
    def calculate(self, chunks_id: List[str], context: EvaluatorContext) -> float:
        total_relevant=len(context.relevant_ids)
        
        if total_relevant==0:
            return 0.0
        
        top_k=chunks_id[:self.k]
        
        found_relevant_count = sum(
            1 for chunk in top_k 
            if chunk in context.relevant_ids
        )
        
        # 4. Calculate the ratio of found vs total possible
        return found_relevant_count / total_relevant