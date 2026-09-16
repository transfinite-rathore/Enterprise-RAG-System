from pydantic import BaseModel
from typing import Optional,Iterable,Dict

class QueryContext(BaseModel):
    user_query:str
    processed_query:str
    dense_embedding:Optional[Iterable[float]] = None
    sparse_embedding:Optional[Dict[int,float]] = None
    requires_reterival:Optional[bool] =None
    langauge:Optional[str]=None