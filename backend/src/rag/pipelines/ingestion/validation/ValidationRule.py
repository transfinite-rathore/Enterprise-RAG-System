from __future__ import annotations
from abc import ABC,abstractmethod
from typing import Dict
from langchain_core.documents import Document

class DocumentValidationRule(ABC):
    @abstractmethod
    def validate_document(self,document:Document):
        pass
    

