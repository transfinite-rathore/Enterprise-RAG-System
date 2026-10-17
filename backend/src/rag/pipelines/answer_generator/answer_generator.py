import uuid
from pydantic import BaseModel
from typing import Iterable
from .prompt_builder import PromptBuilder
from ...model.reranked_context import RerankContext
from ...model.retrieved_document import RetrievedDocument
from ...model.query_context import QueryContext
from .prompt import ANSWER_PROMPT
from ...model.response_context import ResponseContext


class AnswerGenerator:
    
    def __init__(self,model,response_schema:type[BaseModel]) -> None:
        
        if not hasattr(model,"with_structured_output"):
             raise TypeError(
                "Model does not support structured output"
            )
        
        self.chat_model=model.with_structured_output(response_schema)


        
    def generate(self,query:QueryContext,context:Iterable[RetrievedDocument]) -> ResponseContext:
        prompt=PromptBuilder().build(prompt=ANSWER_PROMPT,query=query,contexts=context)
        
        response=self.chat_model.invoke(prompt)
        final_response=ResponseContext(**response.model_dump(),
                        id=str(uuid.uuid4()),
                        user_query=query.user_query,
                        processed_query=query.processed_query
                        )
        
        return final_response
        
        
