import os
from typing import List
from src.rag.pipelines.ingestion.validation.SizeValidation import SizeValidation
from src.rag.pipelines.ingestion.txt_dataloader import TxtDataLoader
from src.rag.pipelines.ingestion.validation.MetadataValidation import MetaDataValidation
from src.rag.pipelines.ingestion.chunking.RecursiveTextSpiltter import RecursiveTextSplitter
from src.rag.pipelines.embedder.sparse_embedder import SparseEmbedderProvider
from src.rag.pipelines.embedder.dense_embedder import DenseEmbedderProvider
from src.rag.pipelines.ingestion.data_processing.normalize_whitespace import NormalizeWhiteSpaceRule
from src.rag.pipelines.ingestion.data_processing.remove_phrase import RemovePhrase
from src.config.qdrant_client import create_qdrant_async_client
from src.config.qdrant_client import create_qdrant_client
from src.rag.factories.vectorstore.VectorStoreFactory import VSFactory
from src.rag.pipelines.ingestion.ingest_data import IngestionPipeline
from src.config.logging_config import set_logger
from src.config.config_manager import get_config
import asyncio

ingestion_config=get_config()["ingestion"]
data=get_config()["paths"]
logger=set_logger(__name__,ingestion_config["logging_file_path"])

# logger = logging.getLogger(__name__)
file_path=data["podcast_data_file_path"]
metadata_file_path=data["podcast_metadata_file_path"]



async def main():
    transcripts=os.listdir(file_path)
    logger.info("Ingesting DATA LOAD_DATA")
    # collection_name="RAG2"

    loader=TxtDataLoader(file_path,metadata_file_path)
    chunker=RecursiveTextSplitter(chk_size=ingestion_config["chunk_size"],chk_overlap=ingestion_config["chunk_overlap"])
    sparse_embedder=SparseEmbedderProvider()
    dense_embedder=DenseEmbedderProvider()
    validators=[SizeValidation(20,5000),MetaDataValidation()]
    cleaners=[RemovePhrase("Transcript:   (disclaimer: may contain unintentionally confusing, inaccurate and/or amusing transcription errors)")
              ,NormalizeWhiteSpaceRule()]

    vs_client=create_qdrant_async_client()        #create_qdrant_client()
    vector_store=VSFactory(vs_client).create_vector_store()

    await vector_store.create_collection()
        
    pipeline=IngestionPipeline(loader,cleaners,validators,chunker,dense_embedder,sparse_embedder,vector_store)  
 
    await pipeline.ingest(ingestion_config["collection_name"])
    await vector_store.close()
        
 
if __name__=="__main__":   
    asyncio.run(main())
    # main()





