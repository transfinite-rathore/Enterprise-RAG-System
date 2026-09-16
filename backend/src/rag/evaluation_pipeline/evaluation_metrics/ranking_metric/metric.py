from abc import ABC,abstractmethod
from typing import List
from ....model.evaluation_context import EvaluatorContext

class BaseRankingMetric(ABC):
    
    @property
    @abstractmethod
    def name(self):
        """Returns the identifier for the metric (e.g., 'precision@5')."""
        pass
    
    @abstractmethod
    def calculate(self,chunks_id:List[str],context:EvaluatorContext)->float:
        pass