from __future__ import annotations
from abc import ABC,abstractmethod

class DataLoader(ABC):
    @abstractmethod
    def load_document(self,path):
        pass
    
# class PDFDataLoader(DataLoader):
    
#     def load_document(self,document):
#         return 
    
# class DataLoaderFactory:
    
#     def get_loader(self,extension):
#         if extension==".pdf":
#             return PDFDataLoader()
