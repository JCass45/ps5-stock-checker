from abc import ABC, abstractmethod
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver

from buyers.models.credit_card import CreditCard


class BaseBuyer(ABC):
    def __init__(self, driver: ChromeDriver, ps5_page_url: str):
        self._driver = driver
        self._ps5_page_url = ps5_page_url

    @abstractmethod
    def buy(self, credit_card: CreditCard):
        pass
