from pathlib import Path
import os
from backend.src.rag.pipelines.ingestion.validation.SizeValidation import SizeValidation
from backend.src.rag.pipelines.ingestion.validation.MetadataValidation import MetaDataValidation
from rag.pipelines.ingestion.HF_dataloader import HFDataLoader
from backend.src.rag.pipelines.ingestion.chunking.RecursiveTextSpiltter import RecursiveTextSplitter
from backend.src.rag.pipelines.Embedding import EmbedderProvider
from config.qdrant_client import create_qdrant_client
from rag.factories.vectorstore.VectorStoreFactory import VSFactory
from rag.pipelines.ingestion.ingest_data import IngestionPipeline
from config.logging_config import set_logger
import logging

logger=set_logger(__name__,"logs/ingestion.log")
# logger = logging.getLogger(__name__)

def main():
    path=Path(os.getcwd()).parents[1]
    data_path=path / "data"/"test"
    
    logger.info("LOGGER TEST FROM LOAD_DATA")
    collection_name="RAG3"
    loader=HFDataLoader(data_path)
    chunker=RecursiveTextSplitter(chk_size=600,chk_overlap=100)
    embedder=EmbedderProvider()
    validators=[SizeValidation(20,5000),MetaDataValidation()]
    

    vs_client=create_qdrant_client()
    vector_store=VSFactory(vs_client).create_vector_store()

    if not vector_store.collection_exists(collection_name):
        vector_store.create_collection(collection_name, size=384)
        
    pipeline=IngestionPipeline(loader,validators,chunker,embedder,vector_store)  
    
    pipeline.ingest(collection_name)
        
 
if __name__=="__main__":   
    main()
    





