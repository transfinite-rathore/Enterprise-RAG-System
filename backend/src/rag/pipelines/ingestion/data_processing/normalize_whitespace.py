from .data_processing_rule import DataCleaningRule
from langchain_core.documents import Document
class NormalizeWhiteSpaceRule(DataCleaningRule):
    
    def clean(self, datarow: Document) -> Document:
        datarow.page_content=" ".join(datarow.page_content.split())
        return datarow