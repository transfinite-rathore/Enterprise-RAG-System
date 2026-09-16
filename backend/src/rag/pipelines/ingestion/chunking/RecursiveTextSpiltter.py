from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .ChunkingStrategy import ChunkingStrategy
from typing import List,Optional,Iterable

class RecursiveTextSplitter(ChunkingStrategy):
    def __init__(self,chk_size:int=250,chk_overlap:int=20,sep_list:Optional[List[str]]=None) -> None:
        if sep_list is None:
            self.sep_list=["\n\n", "\n", " ", ""]
        else:
            self.sep_list=sep_list
        self.splitter=RecursiveCharacterTextSplitter(chunk_size=chk_size, chunk_overlap=chk_overlap,separators=self.sep_list)
    
    def chunk_document(self, document: Document) -> Iterable[Document]:
        return self.splitter.split_documents([document])
        