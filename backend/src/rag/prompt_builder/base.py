from abc import ABC,abstractmethod

class IPromptBuilder(ABC):
    
    def build_prompt(self,**kwargs):
        pass
    pass