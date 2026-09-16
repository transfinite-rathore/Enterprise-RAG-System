
from .ValidationRule import DocumentValidationRule
from langchain_core.documents import Document
from typing import Dict


class SizeValidation(DocumentValidationRule):
    
    def __init__(self,document_min_size:int,document_max_size:int) -> None:
        self.document_min_size=document_min_size
        self.document_max_size=document_max_size

    
    def validate_document(self, document: Document) -> Dict:

        if not isinstance(document.page_content,str):
            return {"is_valid":False, "reason":"Expected string"}
        content_list=document.page_content.split(" ")
        if len(content_list)<self.document_min_size:
            return {"is_valid":False, "reason":"Document Size too small"}
        if len(content_list)>self.document_max_size:
            return {"is_valid":False, "reason":"Document Size too big"}
        return {"is_valid":True}
    