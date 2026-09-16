from .....prompt_builder.base import IPromptBuilder
from .....model.rag_eval_context import RAGEvaluationPayload
from .prompt import prompt

class FaithfullnessPromptBuilder(IPromptBuilder):
    
    def build_prompt(self, context:str,payload:RAGEvaluationPayload):
        # print()
        return prompt.format(context_string=context,generated_answer=payload.response_result["answer"])
        
