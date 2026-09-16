from ..evaluation_pipeline.judges.llm_relevance_judge import LLMRelevanceJudge
from ...config.config_manager import get_config
from ...rag.model.llm_config import LLMConfig
from ..factories.LLMProvider import ChatModelProvider


def create_LLM_judge() -> LLMRelevanceJudge:
    # 1. Find out which provider is currently active (returns "open_router")
    llm=get_config()["llm"]
    active_provider_name = llm["active_provider"]

    # 2. Get the settings for that specific provider
    provider_settings = llm["provider"][active_provider_name]

    # 3. Initialize your config using the nested settings
    llm_config = LLMConfig(
        provider=active_provider_name,                 # "open_router"
        model_name=provider_settings["model_name"],    # "nvidia/nemotron-3-super-120b-a12b:free"
        temperature=provider_settings["temperature"]   # 0.5
    )
        

    llm_model = ChatModelProvider(llm_config).get_model()
    
    return LLMRelevanceJudge(llm_model=llm_model)
