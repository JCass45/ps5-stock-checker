from buyers.models.credit_card import CreditCard
import time
from canaries.base_canary import BaseCanary
from buyers.base_buyer import BaseBuyer

DEFAULT_OUT_OF_STOCK_MESSAGES = [
    "Out of Stock",
    "Out of stock",
    "No stock",
    "out of stock",
    "OUT OF STOCK",
    "Out Of Stock",
]


class Shop:
    def __init__(self, canary: BaseCanary, buyer: BaseBuyer, **params):
        self._canary = canary
        self._buyer = buyer
        self._name = params["name"]
        self._url = params["url"]
        self._out_of_stock_elements = (
            params.get("out_of_stock_elements", []) + DEFAULT_OUT_OF_STOCK_MESSAGES
        )
        self._wait_time = params.get("wait_time", 30)
        self._enabled = params.get("enabled", False)

    def run(self, credit_card: CreditCard):
        while True:
            found = self._canary.search()
            self._buyer.buy(credit_card) if found else time.sleep(self._wait_time)

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @property
    def enabled(self):
        return self._enabled

    @property
    def out_of_stock_elements(self):
        return self._out_of_stock_elements

    @property
    def wait_time(self):
        return self._wait_time
