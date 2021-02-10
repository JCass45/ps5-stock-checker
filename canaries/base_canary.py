from abc import ABC, abstractmethod

from notifier.base_notifier import BaseNotifier
from requests import Session


class BaseCanary(ABC):
    def __init__(self, session: Session, notifier: BaseNotifier, ps5_page_url: str):
        self._session = session
        self._notifier = notifier
        self._ps5_page_url = ps5_page_url

    @abstractmethod
    def search(self) -> bool:
        pass
