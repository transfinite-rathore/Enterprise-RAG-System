from abc import ABC,abstractmethod
from typing import Dict,Any


class FileStoreInterface(ABC):
    
    @abstractmethod
    def save_file(self,run_id:str,file:Any | Dict[str,Any]):
        pass
    
    @abstractmethod
    def load_file(self,run_id:str)-> Any | Dict[str,Any]:
        pass