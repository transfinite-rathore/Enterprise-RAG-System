from abc import abstractmethod,ABC

class LLMFactory(ABC):
    @abstractmethod
    def create_model(self):
        pass
    pass


# we will create each api a wrapper