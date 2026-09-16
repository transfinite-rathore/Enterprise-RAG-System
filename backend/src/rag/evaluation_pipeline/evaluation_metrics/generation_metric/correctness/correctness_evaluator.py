from .....model.evaluation_context import EvaluatorContext
from .....model.rag_eval_context import RAGEvaluationPayload
from .prompt_builder import CorrectnessPromptBuilder
from ..metric import BaseGenerationMetric
import json

class CorrectnessEvaluationMetric(BaseGenerationMetric):
    
    def __init__(self,llm_model) -> None:
        self.model=llm_model
        self.prompt_builder=CorrectnessPromptBuilder()
    
    @property
    def name(self) -> str:
        return "Correctness"
    
    async def compute(self, payload: RAGEvaluationPayload, context: EvaluatorContext) -> float:
        # return await super().compute(payload, context)
        if not payload.expected_answer:
            return 0.0 # Cannot compute correctness without a reference baseline
        prompt=self.prompt_builder.build_prompt(payload=payload)
        response = await self.model.ainvoke(prompt)
        try:
            data = json.loads(response.content)
            # Normalize the 1-5 score to a 0.0 - 1.0 float for metric consistency
            score_out_of_5 = float(data.get("score", 1))
            return (score_out_of_5 - 1) / 4.0 
        except Exception as e:
            print(f"Correctness evaluation failed: {e}")
            return 0.0