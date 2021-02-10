from typing import List
from shops.shop import Shop
from buyers.models.credit_card import CreditCard
from shops.shop_factory import ShopFactory
import os
import time
import requests
import json
from multiprocessing import Process
from bs4 import BeautifulSoup
from notifier.twilio_notifier import TwilioNotifier
from buyers.smyths_ire_buyer import SmythsIreBuyer
from selenium.webdriver import Chrome, ChromeOptions

CONFIG_DIR = "configs/"


def get_stores() -> List[Shop]:
    shops = []
    configs = os.listdir(CONFIG_DIR)
    print(f"Found {len(configs)} configs")
    for store_config in configs:
        with open(f"{CONFIG_DIR}{store_config}") as json_file:
            raw_config = json.load(json_file)
            shops.append(ShopFactory.build_shop(**raw_config))
    valid_shops = list(filter(lambda config: config.enabled is True, shops))
    print(f"Found {len(valid_shops)} enabled stores")
    return valid_shops


if __name__ == "__main__":
    processes = []
    credit_card = CreditCard(
        os.getenv("JACKS_CREDIT_CARD_NUMBER"),
        int(os.getenv("JACKS_CREDIT_CARD_EXPIRATION_MONTH")),
        int(os.getenv("JACKS_CREDIT_CARD_EXPIRATION_YEAR")),
        int(os.getenv("JACKS_CREDIT_CARD_CVV")),
    )
    for store in get_stores():
        p = Process(target=store.run, args=(credit_card,))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()
