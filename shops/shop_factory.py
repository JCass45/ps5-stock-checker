from shops.shop import Shop
from buyers.smyths_ire_buyer import SmythsIreBuyer
from canaries.smyths_ire_canary import SmythsIreCanary
from selenium.webdriver import Chrome, ChromeOptions


class ShopFactory:
    @staticmethod
    def build_shop(shop_config) -> Shop:
        opts = ChromeOptions()
        opts.add_argument("--no-sandbox")
        opts.add_argument("--headless")
        opts.add_argument("--disable-dev-shm-usage")
        selenium_driver = Chrome(options=opts)

        if shop_config.name == "smyths_ire":
            canary = SmythsIreCanary(shop_config.url)
            buyer = SmythsIreBuyer(selenium_driver, shop_config.url)
            return Shop(canary, buyer, **shop_config)
