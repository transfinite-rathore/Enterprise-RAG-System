from ...model.query_context import QueryContext
from ...model.reranked_context import RerankContext
from typing import Iterable
from ...prompt_builder.base import IPromptBuilder
# from base import IPromptBuilder

class PromptBuilder(IPromptBuilder):

    def build(self,prompt:str,contexts:Iterable[RerankContext],query:QueryContext) -> str:
        
        context_text= "/n/n".join([
            f"[ Document id : {context.metadata['document_id']} /n]"
            f"{context.content}" 
            for context in contexts])
        
        return prompt.format(contexts=context_text,user_query=query.user_query,processed_query=query.processed_query)
        