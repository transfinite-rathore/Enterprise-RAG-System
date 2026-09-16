from abc import ABC, abstractmethod
from langchain_core.documents import Document
class DataCleaningRule(ABC):
    
    @abstractmethod
    def clean(self,datarow:Document):
        pass