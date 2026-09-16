from pydantic import BaseModel
from typing import List,Any,Optional
from datetime import datetime
from .retrieved_document import RetrievedDocument
from .reranked_context import RerankContext
from .llm_response import LLMResponse


class RAGResult(BaseModel):
    query:str
    user_id:str
    conversation_id:str
    retrieved_result:List[RetrievedDocument]
    reranked_result:List[RerankContext]
    response_result:LLMResponse
    metadata:Optional[dict[str,Any]] = None
    
        
    