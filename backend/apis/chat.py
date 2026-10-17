from contextlib import asynccontextmanager
from fastapi import FastAPI,APIRouter, HTTPException, Depends
from .models.model import *
from ..src.rag.factories.rag_factory import create_rag_orchestrator
from ..src.rag.pipelines.resultstore.file_result_store import RAGFileResultStore
import uuid

router = APIRouter(prefix="/api/v1/rag", tags=["RAG Application"])

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. STARTUP: Unpack the tuple
    print("Bootstrapping RAG pipeline and Vector Store...")
    vector_store, rag = create_rag_orchestrator()
    
    # 2. STATE INJECTION: Yield the objects your routes need
    yield {"rag": rag}
    
    # 3. SHUTDOWN: Close the database connection gracefully
    print("Shutting down Vector Store connections...")
    if hasattr(vector_store, "close"):
        vector_store.close()
        
def get_result_saver():
    return RAGFileResultStore()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest, 
    orchestrator = Depends(create_rag_orchestrator)
):
    """
    Main endpoint for user interactions. Returns only the generated answer.
    """
    try:
        # If no conversation_id is passed, create a new one
        conv_id = request.conversation_id or str(uuid.uuid4())
        
        # Invoke your pipeline (assuming your invoke method accepts these)
        run_id, response_text = orchestrator.invoke(
            user_id=request.user_id,
            query=request.query,
            # Pass conv_id to your orchestrator if it supports it
        )
        
        return ChatResponse(
            conversation_id=conv_id,
            run_id=run_id,
            answer=response_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/insights/{run_id}", response_model=RunInsightsResponse)
async def get_run_insights(
    run_id: str, 
    rs = Depends(get_result_saver)
):
    """
    Fetches the underlying metadata, latency, and chunks for a specific query run.
    Ideal for admin dashboards or 'Explain this answer' features.
    """
    # Assuming your result_saver has a method to fetch a run by ID
    rag_result = rs.result_saver.load(run_id)
    
    if not rag_result:
        raise HTTPException(status_code=404, detail="Run ID not found")
        
    return RunInsightsResponse(
        run_id=run_id,
        conversation_id=rag_result.conversation_id,
        query=rag_result.query,
        retrieved_chunks_count=len(rag_result.retrieved_result),
        reranked_chunks_count=len(rag_result.reranked_result),
        retrieved_results=[doc.model_dump() for doc in rag_result.retrieved_result],
        reranked_results=[doc.model_dump() for doc in rag_result.reranked_result],
        latency=rag_result.metadata 
    )