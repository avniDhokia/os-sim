from abc import ABC, abstractmethod

# abstract IODevice class to be extended by use-able io devices
class IODevice(ABC):

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_block_queue(self):
        pass

    @abstractmethod
    def 
