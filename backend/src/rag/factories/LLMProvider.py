from .chatmodel.OpenRouterLLM import OpenRouterLLM
from ..model.llm_config import LLMConfig

LLM_REGISTRY={
    "open_router":OpenRouterLLM
}

class ChatModelProvider:
    
    def __init__(self,config:LLMConfig) -> None:
        self.config=config
        
    def get_model(self):
    
        model=LLM_REGISTRY.get(self.config.provider.lower())
        if model is None:
            raise ValueError(
                f"Unsupported provider: {self.config.provider}"
            )
            
        return model(self.config).create_model()