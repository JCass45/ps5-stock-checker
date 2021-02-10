from buyers.smyths_ire_buyer import SmythsIreBuyer
from canaries.smyths_ire_canary import SmythsIreCanary
from notifier.twilio_notifier import TwilioNotifier
from selenium.webdriver import Chrome, ChromeOptions

from shops.shop import Shop


class ShopFactory:
    @staticmethod
    def build_shop(shop_config) -> Shop:
        opts = ChromeOptions()
        opts.add_argument("--no-sandbox")
        opts.add_argument("--headless")
        opts.add_argument("--disable-dev-shm-usage")
        selenium_driver = Chrome(options=opts)

        notifier = TwilioNotifier()

        if shop_config.name == "smyths_ire":
            canary = SmythsIreCanary(notifier, shop_config.url)
            buyer = SmythsIreBuyer(selenium_driver, shop_config.url)
            return Shop(canary, buyer, **shop_config)
