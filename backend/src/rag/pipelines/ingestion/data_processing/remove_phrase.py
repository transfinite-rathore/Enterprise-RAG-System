from .data_processing_rule import DataCleaningRule
from langchain_core.documents import Document

class RemovePhrase(DataCleaningRule):
    
    def __init__(self,phrase:str) -> None:
        self.phrase=phrase

    
    def clean(self, datarow: Document) -> Document:
        datarow.page_content= datarow.page_content.replace(self.phrase,"")
        return datarow
