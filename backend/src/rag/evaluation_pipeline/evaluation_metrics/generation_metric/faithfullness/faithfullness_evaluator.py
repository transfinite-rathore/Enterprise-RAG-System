from .....model.evaluation_context import EvaluatorContext
from .....model.rag_eval_context import RAGEvaluationPayload
from .prompt_builder import FaithfullnessPromptBuilder
import json
from ..metric import BaseGenerationMetric

class FaithfullnessEvaluationMetric(BaseGenerationMetric):
    
    def __init__(self,llm_model) -> None:
        self.llm=llm_model
        self.prompt_builder=FaithfullnessPromptBuilder()
        
    @property
    def name(self) -> str:
        return "Faithfulness"
    
    async def compute(self, payload: RAGEvaluationPayload, context: EvaluatorContext) -> float:

        relevant_content=[chunk["content"] for chunk in payload.retrieved_result if chunk["chunk_id"] in context.relevant_ids]
        if len(relevant_content)==0:
            return 0.0 
        
        relevant_context="/n---/n".join(relevant_content)
        prompt=self.prompt_builder.build_prompt(context=relevant_context,payload=payload)
        response=await self.llm.ainvoke(prompt)
        try:
            data = json.loads(response.content)
                    # Normalize the 1-5 score to a 0.0 - 1.0 float for metric consistency
            score_out_of_5 = float(data.get("score", 1))
            return (score_out_of_5 - 1) / 4.0 
        except Exception as e:
            print(f"Faithfulness evaluation failed: {e}")
            return 0.0
        
        return response.content