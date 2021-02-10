import requests
from bs4 import BeautifulSoup
from notifier.base_notifier import BaseNotifier
from retrying import retry

from canaries.base_canary import BaseCanary


class SmythsIreCanary(BaseCanary):
    def __init__(self, notifier: BaseNotifier, ps5_page_url: str):
        session = requests.Session()
        session.headers.update(
            {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
            }
        )
        super().__init__(session, notifier, ps5_page_url)

    @retry(stop_max_delay=(1000 * 60 * 5), wait_fixed=(1000))
    def search(self) -> bool:
        response = self._session.get(self._ps5_page_url)
        if response.ok:
            text = response.text
            html = BeautifulSoup(text, "html.parser")
            addToCartForm = html.find(id="customAddToCartForm")
            addToCartButton = addToCartForm.find(id="addToCartButton")
            return addToCartButton != None
        else:
            response.raise_for_status()
