from .llm_response import LLMResponse

class ResponseContext(LLMResponse):
    id:str
    user_query:str
    processed_query:str

    