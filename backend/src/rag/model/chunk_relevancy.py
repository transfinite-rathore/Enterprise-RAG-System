from pydantic import BaseModel,Field
from typing import Optional

class ChunkRelevantVerdict(BaseModel):
    chunk_id:str
    is_relevant:bool
    reason:str
    score:int = Field(default=1,ge=0,le=5)
    