from pydantic import BaseModel

class LLMResponse(BaseModel):
    answer: str
    citations: list[str]