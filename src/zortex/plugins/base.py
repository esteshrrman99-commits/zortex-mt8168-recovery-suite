from abc import ABC,abstractmethod
class ZortexPlugin(ABC):
    name='unnamed'; version='0.0.0'
    @abstractmethod
    def analyze(self,context): raise NotImplementedError
