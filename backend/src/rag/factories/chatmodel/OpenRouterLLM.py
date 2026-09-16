from langchain_openrouter import ChatOpenRouter
from .LLMFactory import LLMFactory
from ...model.llm_config import LLMConfig
import os
from dotenv import load_dotenv

load_dotenv()


class OpenRouterLLM(LLMFactory):
    
    def __init__(self,config:LLMConfig) -> None:
        self.config=config
    
    def create_model(self):
        model=ChatOpenRouter(
            model=self.config.model_name,
            temperature=self.config.temperature,
            api_key=os.getenv("OPEN_ROUTER_API_KEY") # pyright: ignore[reportArgumentType])
        )
        
        return model