from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Request/Response Models for Chat ---
class ChatRequest(BaseModel):
    user_id: str
    query: str
    conversation_id: Optional[str] = None # None if starting a new chat

class ChatResponse(BaseModel):
    conversation_id: str
    run_id: str  # Link to the specific generation run
    answer: str

# --- Response Models for Metadata/Insights ---
class LatencyMetrics(BaseModel):
    query_preprocessing_latency: float
    retrieval_latency: float
    reranking_latency: float
    generation_latency: float
    total_execution_time: float

class RunInsightsResponse(BaseModel):
    run_id: str
    conversation_id: str
    query: str
    retrieved_chunks_count: int
    reranked_chunks_count: int
    retrieved_results: List[Dict[str, Any]]
    reranked_results: List[Dict[str, Any]]
    latency: LatencyMetrics