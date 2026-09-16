from typing import Iterable,Optional,Dict
from sentence_transformers import SparseEncoder
from langchain_core.documents import Document
from ....config.config_manager import get_config
from .base import BaseEmbedderProvider

class SparseEmbedderProvider(BaseEmbedderProvider):
    default_model_path=get_config()["paths"]["sparse_model_path"]
    
    def __init__(self,embedder_model_path:Optional[str]=None) -> None:
        self.embedder_model_path = (embedder_model_path or self.default_model_path)
        self.embedder=SparseEncoder(self.embedder_model_path)
     
    def _convert_sparse_embedding(self, embedding) -> Dict[int, float]:
        embedding = embedding.coalesce()

        indices = embedding.indices()[0].tolist()
        values = embedding.values().tolist()

        return {
            int(index): float(value)
            for index, value in zip(indices, values)
        }

    def embed_document(
        self,
        chunks: Iterable[Document]
    ) -> list[Dict[int, float]]:

        texts = [chunk.page_content for chunk in chunks]

        sparse_embeddings = self.embedder.encode(
            texts,
            batch_size=32
        )

        return [
            self._convert_sparse_embedding(embedding)
            for embedding in sparse_embeddings
        ]

    def embed_query(self, query: str) -> Dict[int, float]:

        sparse_embedding = self.embedder.encode(query)

        return self._convert_sparse_embedding(sparse_embedding)