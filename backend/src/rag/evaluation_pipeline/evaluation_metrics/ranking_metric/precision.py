from typing import List
from ....model.evaluation_context import EvaluatorContext
from ....evaluation_pipeline.evaluation_metrics.ranking_metric.metric import BaseRankingMetric

class PrecisionAtK(BaseRankingMetric):
    
    
    def __init__(self,k:int=5) -> None:
        self.k=k
    
    @property
    def name(self):
        return f"Precison@{self.k}"
    
    def calculate(self, chunks_id: List[str], context: EvaluatorContext) -> float:
        top_k=chunks_id[:self.k]
        
        if not top_k:
            return 0.0
        
        relevant_count=sum(1 for chunk in top_k if chunk in context.relevant_ids)
        return relevant_count/len(top_k)
