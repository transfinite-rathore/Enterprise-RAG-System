from typing import Iterable,Optional
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document
from ....config.config_manager import get_config
from .base import BaseEmbedderProvider

class DenseEmbedderProvider(BaseEmbedderProvider):
    default_model_path=get_config()["paths"]["dense_model_path"]
    def __init__(self,embedder_model_path:Optional[str]=None) -> None:
        self.embedder_model_path = (embedder_model_path or self.default_model_path)
        self.embedder=SentenceTransformer(self.embedder_model_path)
    
    def embed_document(self,chunks:Iterable[Document]) -> Iterable[float]:
        text=[chunk.page_content for chunk in chunks]
        return self.embedder.encode(text,batch_size=32,convert_to_numpy=True)

    
    def embed_query(self,query:str) -> Iterable[float]:
        return self.embedder.encode(query,convert_to_numpy=True)