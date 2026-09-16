from src.rag.factories.rag_factory import create_rag_orchestrator
import traceback

    
if __name__ == "__main__":

    query="can you tell me total number of people working in Spacex"
    
    vector_store,rag=create_rag_orchestrator()
    try:
        response=rag.invoke("123",query)
        print(response)
    except Exception as e:
        print("Exception", e)
        traceback.print_exc()
    finally:
        vector_store.close()
    