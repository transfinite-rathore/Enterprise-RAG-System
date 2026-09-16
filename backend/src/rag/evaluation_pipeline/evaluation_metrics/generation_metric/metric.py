from abc import ABC, abstractmethod
from ....model.rag_eval_context import RAGEvaluationPayload
from ....model.evaluation_context import EvaluatorContext


class BaseGenerationMetric(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the identifier for the metric (e.g., 'faithfulness')."""
        pass

    @abstractmethod
    async def compute(self, payload: RAGEvaluationPayload, context: EvaluatorContext) -> float:
        """Evaluates the generated text asynchronously using an LLM."""
        pass