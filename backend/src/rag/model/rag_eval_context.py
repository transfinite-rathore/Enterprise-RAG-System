from pydantic import BaseModel,Field
from typing import Optional,List,Any

class RAGEvaluationPayload(BaseModel):
    
    user_id:str
    conversation_id:str
    expected_answer:Optional[str]=None
    query:str
    retrieved_result:List=Field(default_factory=list)
    reranked_result:List=Field(default_factory=list)
    response_result:dict[str,Any]
    metadata:dict[str,Any]
    