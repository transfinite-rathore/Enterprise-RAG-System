from ....config.logging_config import set_logger
import asyncio
from typing import List
from .data_processing.data_processing_rule import DataCleaningRule
from .validation.ValidationRule import DocumentValidationRule
from multiprocessing import Queue,Process,current_process
from ....config.config_manager import get_config
import time
logger=set_logger(__name__,get_config()["ingestion"]["logging_file_path"])

# logger= logging.getLogger(__name__)



## WORKER OUTSIDE CLASS
def chunks_worker(document_queue:Queue,chunking_queue:Queue,chunker):
        document_count=0
        chunk_count=0
        while True:
            try:
                document=document_queue.get()
                if document is None:
                    chunking_queue.put(None)
 
                    break
                document_count+=1
                chunks=chunker.chunk_document(document)
                for chunk in chunks:
                    chunking_queue.put(chunk)
                    chunk_count+=1
                if document_count % 20 == 0:
                    logger.info(
                        "%s progress | Documents=%d | Chunks=%d",
                        current_process().name,
                        document_count,
                        chunk_count,
                    )
            except Exception as e:
                logger.exception(e)
        logger.info(f'''Chunking Completed Successfully by {current_process().name} , 
                    document served {document_count} and chunks produced {chunk_count}''')

## WORKER OUTSIDE CLASS
def load_document(loader,validator,cleaner:List[DataCleaningRule],document_queue,chunking_worker):
    doc_count=0
    for document in loader.load_document():
        # print(document)
        try:
            for rule in cleaner:
                document=rule.clean(document)
            if not all(
                        rule.validate_document(document)
                        for rule in validator
                            ):
                continue
            
                
                
            doc_count+=1
            document_queue.put(document)
            if doc_count%20==0:
                logger.info(f"{doc_count} number of document loaded till now")
        except Exception as e:
            logger.exception(e)
    logger.info("All documents are loaded!")
    for _ in range(chunking_worker):
        document_queue.put(None)
        


## UTILISING MULTIPROCESSING FOR CHUNKING(LOADER AND CHUNKER are Process)

class IngestionPipeline:

    def __init__(
        self,
        loader,
        cleaner:List[DataCleaningRule],
        validator:List[DocumentValidationRule],
        chunker,
        dense_embedder,
        sparse_embeder,
        vector_store,
        chunking_worker:int=3
    ):
        self.loader=loader
        self.validator=validator
        self.cleaner=cleaner
        self.chunker=chunker
        self.den_embedder=dense_embedder
        self.sp_embedder=sparse_embeder
        self.vector_store=vector_store
        self.document_queue=Queue(maxsize=1000)
        self.chunking_queue=Queue(maxsize=1000)
        self.chunking_worker=chunking_worker
        
    async def flush_batch(self, batch, collection_name):
        dense_embeddings = self.den_embedder.embed_document(batch)
        sparse_embeddings = self.sp_embedder.embed_document(batch)

        max_attempts = 3
        retry_delay = 2

        for attempt in range(1, max_attempts + 1):
            try:
                await self.vector_store.save_documents(
                    dense_embeddings=dense_embeddings,
                    sparse_embeddings=sparse_embeddings,
                    collection_name=collection_name,
                    chunks=batch,
                )

                logger.info(
                    "Qdrant insertion successful | chunks=%d | attempt=%d",
                    len(batch),
                    attempt,
                )

                batch.clear()
                return

            except Exception as e:
                logger.warning(
                    "Qdrant insertion failed | attempt=%d/%d | "
                    "retrying in %ds | error=%s",
                    attempt,
                    max_attempts,
                    retry_delay,
                    e,
                )

                if attempt == max_attempts:
                    logger.exception(
                        "Qdrant insertion permanently failed | chunks=%d",
                        len(batch),
                    )
                    raise

                time.sleep(retry_delay)

    # def flush_batch(self, batch, collection_name):
    #     dense_embeddings = self.den_embedder.embed_document(batch)
    #     sparse_embeddings = self.sp_embedder.embed_document(batch)

    #     max_attempts = 3
    #     retry_delay = 2

    #     for attempt in range(1, max_attempts + 1):
    #         try:
    #             self.vector_store.save_documents(
    #                 dense_embeddings=dense_embeddings,
    #                 sparse_embeddings=sparse_embeddings,
    #                 collection_name=collection_name,
    #                 chunks=batch,
    #             )

    #             logger.info(
    #                 "Qdrant insertion successful | chunks=%d | attempt=%d",
    #                 len(batch),
    #                 attempt,
    #             )

    #             batch.clear()
    #             return

    #         except Exception as e:
    #             logger.warning(
    #                 "Qdrant insertion failed | attempt=%d/%d | "
    #                 "retrying in %ds | error=%s",
    #                 attempt,
    #                 max_attempts,
    #                 retry_delay,
    #                 e,
    #             )

    #             if attempt == max_attempts:
    #                 logger.exception(
    #                     "Qdrant insertion permanently failed | chunks=%d",
    #                     len(batch),
    #                 )
    #                 raise

    #             time.sleep(retry_delay)
    
    async def process_chunk_queue(self, collection_name, batch_size=32):
        finished_workers = self.chunking_worker
        batch = []
        stored_chunks = 0
        
        while True:

            chunk = self.chunking_queue.get()
            if chunk is None:
                finished_workers -= 1
                if finished_workers == 0:
                    break
                continue
            batch.append(chunk)
            
            
            if len(batch) >= batch_size:
                stored_chunks += batch_size   
                await self.flush_batch(batch, collection_name)
                logger.info(
                "Total chunks stored: %d",
                stored_chunks
                )

        if batch:
            stored_chunks += len(batch)
            await self.flush_batch(batch, collection_name)
        logger.info(
        "Chunk processing completed | Total chunks stored=%d",
        stored_chunks
        )
            
    async def ingest(self,collection_name):
        # self.load_document(path) ,loader,validator,document_queue,chunking_worker)
        logger.info(
            "Starting ingestion | Chunk Workers=%d | Collection=%s",
            self.chunking_worker,
            collection_name,
        )
        loader=Process(target=load_document,args=(self.loader,self.validator,self.cleaner,self.document_queue,self.chunking_worker))
        
        workers=[]
        for _ in range(self.chunking_worker):
            chunker=Process(target=chunks_worker,args=(self.document_queue,self.chunking_queue,self.chunker))
            chunker.start()
            logger.info(
            "Chunk Worker-%d started (PID=%d)",
                _ + 1,
            chunker.pid,
            )   
            workers.append(chunker)
            
            # chunker.join()
        loader.start()
        logger.info("Loader process started")
        await self.process_chunk_queue(collection_name)

        # embedder=Process(target=embedding_worker,args=(self.chunking_worker,self.chunking_queue,collection_name))
        
        # embedder.start()
        loader.join()
        for worker in workers:
            worker.join()
        # embedder.join()        

     
#############################################################################################
############## SEQUENTIAL EXECUTION OF DATA INGESTION #######################################
#############################################################################################   
    # class BatchManager:

    # def __init__(self, batch_size: int = 256):
    #     self.batch_size = batch_size
    #     self._chunks: List[Document] = []

    # def add(self, chunks: List[Document]) -> None:
    #     self._chunks.extend(chunks)

    # def should_flush(self) -> bool:
    #     return len(self._chunks) >= self.batch_size

    # def flush(self) -> List[Document]:
    #     batch = self._chunks[: self.batch_size]
    #     self._chunks = self._chunks[self.batch_size :]
    #     return batch

    # def flush_remaining(self) -> List[Document]:
    #     batch = self._chunks
    #     self._chunks = []
    #     return batch

    # def is_empty(self) -> bool:
    #     return len(self._chunks) == 0

    # @property
    # def size(self) -> int:
    #     return len(self._chunks)
    
    
    
    # def ingest_data(self, path, collection_name):

    #     failed = 0
    #     processed = 0
    #     stored = 0
    #     skipped = 0

    #     batch_manager = BatchManager(batch_size=64)

    #     logger.info("Starting ingestion")

    #     for document in self.loader.load_document(path):

    #         processed += 1

    #         try:

    #             if not all(
    #                 rule.validate_document(document)
    #                 for rule in self.validator
    #             ):
    #                 skipped += 1
    #                 continue

    #             chunks = self.chunker.chunk_document(document)

    #             batch_manager.add(chunks)

    #             if batch_manager.should_flush():

    #                 batch = batch_manager.flush()

    #                 embeddings = self.embedder.embed_document(batch)

    #                 self.vector_store.save_documents(
    #                     embeddings,
    #                     collection_name,
    #                     batch
    #                 )

    #                 stored += len(batch)

    #             if processed % 1000 == 0:
    #                 logger.info(
    #                     "Processed=%d Stored=%d Skipped=%d Failed=%d Buffer=%d",
    #                     processed,
    #                     stored,
    #                     skipped,
    #                     failed,
    #                     batch_manager.size,
    #                 )

    #         except Exception:

    #             failed += 1

    #             logger.exception(
    #                 "Failed processing document %s",
    #                 document.metadata.get("document_id", "Unknown")
    #             )

    # # Flush remaining chunks

    #     if not batch_manager.is_empty():

    #         batch = batch_manager.flush_remaining()

    #         embeddings = self.embedder.embed_document(batch)

    #         self.vector_store.save_documents(
    #             embeddings,
    #             collection_name,
    #             batch
    #         )

    #         stored += len(batch)

    #     logger.info(
    #         "Finished Ingestion | Processed=%d Stored=%d Skipped=%d Failed=%d",
    #         processed,
    #         stored,
    #         skipped,
    #         failed,
    #     )


