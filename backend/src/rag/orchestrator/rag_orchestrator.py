import uuid
import time
from datetime import datetime
from typing import Optional
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
                 retriever:Retriever,result_generator:AnswerGenerator,
                 result_saver:RAGResultStore,reranker:Optional[Reranker]=None):

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
        print("Process started")
        process_starting_time=time.perf_counter()
        processed_query_context=self.query_processor.preprocess(query_context)
        print("processing done")
        query_processing_time=time.perf_counter()
        documents=self.retriever.retrieve(processed_query_context)
        retrieval_time=time.perf_counter()
        print("reterival done")
        if self.reranker:
            final_documents=self.reranker.rerank(processed_query_context,documents)
            reranking_time=time.perf_counter()
            saved_reranked_result=list(final_documents)
            print("reranking done")
        else:
            final_documents=documents
            saved_reranked_result=[]
        response=self.result_generator.generate(processed_query_context,final_documents)
        response_time=time.perf_counter()
        print("response done")
        
        rag_result=RAGResult(
            query=query,
            user_id=user_id,
            conversation_id=conv_id,
            retrieved_result=documents,
            reranked_result=saved_reranked_result,
            response_result=response,
            metadata={
                      "starting_time":start_time,
                      "query_preprocessing_latency":query_processing_time-process_starting_time,
                      "retrieval_latency":retrieval_time-query_processing_time,
                      "reranking_latency":reranking_time-retrieval_time,
                      "generation_latency":response_time-reranking_time,
                      "total_execution_time":response_time-query_processing_time,
                      "completion_time":datetime.now()
                      }
                  )
        manifest_details={
            "dense_embedding_model":get_config()["models"]["dense_embedding_model"],
            "sparse_embedding_model":get_config()["models"]["sparse_embedding_model"],
            "collection_name":self.retriever.collection_name,
            "retrieval_strategy":self.retriever.__class__.__name__,
            "retrieval_top_k":self.retriever.top_k,
            "reranker_rule":self.reranker.rerank_rule.__class__.__name__ if self.reranker else None,
            "reranker_model":get_config()["models"]["reranker"],
            "reranker_top_k":getattr(self.reranker,"top_k",None),
            "generator": get_config()["llm"]["provider"][get_config()["llm"]["active_provider"]]["model_name"]
            
            
        }
        run_id=self.result_saver.save(rag_result=rag_result,manifest_details=manifest_details)
        
        return run_id,response
        
        # return response
        
        
        

        

