from .....prompt_builder.base import IPromptBuilder
from  .....model.rag_eval_context import RAGEvaluationPayload
from .prompt import prompt

class AnswerRelevancyPromptBuilder(IPromptBuilder):
    
    def build_prompt(self, payload:RAGEvaluationPayload):
        return prompt.format(query=payload.query,generated_answer=payload.response_result["answer"])
        
