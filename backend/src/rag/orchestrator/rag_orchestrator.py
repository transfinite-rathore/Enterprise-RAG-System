import uuid
from datetime import datetime
from ...config.config_manager import get_config
from ..model.user_query import UserQuery
from ..model.rag_result import RAGResult
from ..pipelines.querypipeline.processor import QueryPipeline 
from ..pipelines.retriever.retriever import Retriever
from ..pipelines.reranker.reranker import Reranker
from ..pipelines.answer_generator.answer_generator import AnswerGenerator
from ..pipelines.resultstore.result_store import RAGResultStore

class RAGOrchestrator:
    
    def __init__(self,query_processor:QueryPipeline,
                 retriever:Retriever,reranker:Reranker,
                 result_generator:AnswerGenerator,result_saver:RAGResultStore):

        self.query_processor=query_processor
        self.retriever=retriever
        self.reranker=reranker
        self.result_generator=result_generator
        self.result_saver=result_saver
        
    
    def invoke(self,user_id:str,query:str):

        
        start_time=datetime.now()
        conv_id=str(uuid.uuid4())
        query_context=UserQuery(
            query=query,
            conversation_id=conv_id,
            user_id=user_id
        )
        processed_query_context=self.query_processor.preprocess(query_context)
        documents=self.retriever.retrieve(processed_query_context)

        reranked_context=self.reranker.rerank(processed_query_context,documents)

        response=self.result_generator.generate(processed_query_context,reranked_context)
        
        rag_result=RAGResult(
            query=query,
            user_id=user_id,
            conversation_id=conv_id,
            retrieved_result=documents,
            reranked_result=list(reranked_context),
            response_result=response,
            metadata={"starting_time":start_time,
                      "completion_time":datetime.now()}
                  )
        manifest_details={
            "dense_embedding_model":get_config()["models"]["dense_embedding_model"],
            "sparse_embedding_model":get_config()["models"]["sparse_embedding_model"],
            "collection_name":self.retriever.collection_name,
            "retrieval_strategy":self.retriever.__class__.__name__,
            "retrieval_top_k":self.retriever.top_k,
            "reranker_rule":self.reranker.rerank_rule.__class__.__name__,
            "reranker_model":get_config()["models"]["reranker"],
            "reranker_top_k":self.reranker.top_k,
            "generator": get_config()["llm"]["provider"][get_config()["llm"]["active_provider"]]["model_name"]
            
            
        }
        self.result_saver.save(rag_result=rag_result,manifest_details=manifest_details)
        
        return response
        
        # return response
        
        
        

        

