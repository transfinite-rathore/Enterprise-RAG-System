from typing import List

from ....model.evaluation_context import EvaluatorContext
from ....evaluation_pipeline.evaluation_metrics.ranking_metric.metric import BaseRankingMetric


'''
Evaluates how far down the list the first relevant document is. If the first relevant chunk is at rank 1, MRR is 1.0. If it is at rank 3, MRR is 0.33.
'''

class MeanReciprocalRank(BaseRankingMetric):

    
    @property
    def name(self):
        return f"MeanReciprocalRank"
    
    def calculate(self, chunks_id: List[str], context: EvaluatorContext) -> float:
        
        for rank,chunk in enumerate(chunks_id,start=1):
            if chunk in context.relevant_ids:
                return 1.0/rank
        return 0.0
