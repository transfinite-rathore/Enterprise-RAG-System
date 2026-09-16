from pydantic import BaseModel,Field

class LLMConfig(BaseModel):
    provider:str
    model_name:str
    temperature:float=Field(ge=0,le=2)