from typing import List,Dict
from .evaluation_metrics.ranking_metric.metric import BaseRankingMetric
from ..model.evaluation_context import EvaluatorContext

class RerankerEvaluator:
    def __init__(self, metrics: List[BaseRankingMetric]):
        self.metrics = metrics

    def evaluate(self, chunks_id:List[str], context: EvaluatorContext) -> Dict[str, float]:
        results = {}
        for metric in self.metrics:
            results[metric.name] = metric.calculate(chunks_id, context)
        return results