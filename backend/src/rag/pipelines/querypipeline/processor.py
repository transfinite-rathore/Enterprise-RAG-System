from ...model.query_context import QueryContext
from .validator.validator import QueryValidator
from .corrector.corrector import QueryCorrecter
from .rewriter.rewriter import QueryRewriter
from ..embedder.base import BaseEmbedderProvider
from typing import Dict



class QueryPipeline:
    
    def __init__(self,
                 validator:QueryValidator,
                 corrector:QueryCorrecter,
                 rewriter:QueryRewriter,
                 dense_embedder:BaseEmbedderProvider,
                 sparse_embedder:BaseEmbedderProvider) -> None:
        self.rewriter=rewriter
        self.validator=validator
        self.corrector=corrector
        self.dense_embedder=dense_embedder
        self.sparse_embedder=sparse_embedder
    
    def preprocess(self,user_query) -> QueryContext:
        validation_result=self.validator.apply_validation(user_query)
        
        if False in validation_result.values():
            raise Exception("Query Validation Failed",validation_result)
        
        updated_query=self.corrector.correct(user_query)
        
        new_query=self.rewriter.rewrite_query(updated_query["corrected_query"])
        
        dense_query_embedding=self.dense_embedder.embed_query(new_query.processed_query)
        sparse_query_embedding=self.sparse_embedder.embed_query(new_query.processed_query)
        new_query=new_query.model_copy(update={
            "dense_embedding":dense_query_embedding,
            "sparse_embedding":sparse_query_embedding
        })
        return new_query
