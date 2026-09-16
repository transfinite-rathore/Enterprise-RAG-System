from pydantic import BaseModel
from typing import Optional

class RetrievedDocument(BaseModel):
    chunk_id:str
    # original_doc_id:str
    content:str
    score:float
    metadata:dict ={}