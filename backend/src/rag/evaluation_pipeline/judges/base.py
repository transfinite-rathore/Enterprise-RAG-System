from abc import ABC, abstractmethod
from typing import Optional,List,Dict
from ...model.retrieved_document import RetrievedDocument
from  ...model.chunk_relevancy import ChunkRelevantVerdict

class RelevanceJudge(ABC):
    @abstractmethod
    async def judge_chunks(self,chunks:List[RetrievedDocument],query:str,human_response=Optional[str])-> Dict[str,ChunkRelevantVerdict]:
        pass

