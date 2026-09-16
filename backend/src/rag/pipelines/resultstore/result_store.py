from abc import ABC,abstractmethod

class RAGResultStore(ABC):
    @abstractmethod
    def save(self,rag_result):
        pass