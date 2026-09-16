# evaluators/generator.py
import asyncio
from typing import List, Dict
from .evaluation_metrics.generation_metric.metric import BaseGenerationMetric
from ..model.rag_eval_context import RAGEvaluationPayload
from ..model.evaluation_context import EvaluatorContext


class GeneratorEvaluator:
    def __init__(self, metrics: List[BaseGenerationMetric]):
        self.metrics = metrics

    async def evaluate(self, payload: RAGEvaluationPayload, context: EvaluatorContext) -> Dict[str, float]:
        if not self.metrics:
            return {}

        # Run all generation metrics concurrently across the network
        scores = await asyncio.gather(
            *(metric.compute(payload, context) for metric in self.metrics)
        )
        return {metric.name: score for metric, score in zip(self.metrics, scores)}