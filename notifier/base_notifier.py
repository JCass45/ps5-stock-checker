from abc import ABC, abstractmethod


class BaseNotifier(ABC):
    @abstractmethod
    def notify(self, message: str, recipient: str, sender: str):
        pass
