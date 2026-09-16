from .ValidationRule import DocumentValidationRule
from langchain_core.documents import Document

class MetaDataValidation(DocumentValidationRule):
    
    def validate_document(self, document: Document):
        if not document.metadata.get("title"):
            return {
                "is_valid": False,
                "reason": "Empty or missing source type"
            }
        # if not document.metadata["title"] or document.metadata["title"]=="":
        #     return {"is_valid":False,"reason":"Empty or missing title"}
        # if not document.metadata["source_type"] or document.metadata["source_type"]=="":
        #     return {"is_valid":False,"reason":"Empty or missing source type"}
        return True
