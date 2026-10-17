import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from .LLMFactory import LLMFactory
from ...model.llm_config import LLMConfig


load_dotenv()


class GroqLLM(LLMFactory):
    
    def __init__(self,config:LLMConfig) -> None:
        self.config=config
    
    def create_model(self):
        model=ChatGroq(
            model=self.config.model_name,
            temperature=self.config.temperature,
            api_key=os.getenv("GROQ_AI_KEY") # pyright: ignore[reportArgumentType])
        )
        
        return model
