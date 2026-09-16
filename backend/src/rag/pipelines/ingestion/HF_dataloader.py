from __future__ import annotations
from typing import List,Iterable
from langchain_core.documents import Document
from ...factories.DataLoader import DataLoader
from datasets import load_from_disk


class HFDataLoader(DataLoader):
    
    def __init__(self,file_path:str) -> None:
        self.file_path=file_path
        super().__init__()
    
    def load_document(self) -> Iterable[Document] :
        try:
            data=load_from_disk(self.file_path)
            for row in data:
                yield Document(
                    page_content=row["content"],
                    metadata={"document_id":row["doc_id"],"title":row["title"],"source_type":row["source_type"]}
                )

        except Exception as e:
            print(e)
            # raise FileNotFoundError()