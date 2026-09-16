from abc import ABC, abstractmethod

class QueryCorrectionRule(ABC):
    @abstractmethod
    def correct(self,query):
        pass
