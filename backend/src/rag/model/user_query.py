from pydantic import BaseModel,Field
from typing import List,Optional,Iterable

class UserQuery(BaseModel):
    user_id:str
    query:str=Field(max_length=512, min_length=1)
    conversation_id:str | None=None
    language:Optional[str]=None