from ...prompt_builder.base import IPromptBuilder
from .judge_prompt import prompt

class PromptBuilder(IPromptBuilder):
    
    def build_prompt(self,query:str,answer:str,context_chunks):
         
        return prompt.format(query=query,human_answer=answer,formatted_chunks_json=context_chunks)
