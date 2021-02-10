import json
import os
from multiprocessing import Process
from typing import List

from dotenv import load_dotenv

from buyers.models.credit_card import CreditCard
from shops.shop import Shop
from shops.shop_factory import ShopFactory

CONFIG_DIR = "configs/"


def get_stores() -> List[Shop]:
    shops = []
    configs = os.listdir(CONFIG_DIR)
    print(f"Found {len(configs)} configs")
    for store_config in configs:
        with open(f"{CONFIG_DIR}{store_config}") as json_file:
            raw_config = json.load(json_file)
            shops.append(ShopFactory.build_shop(raw_config))
    valid_shops = list(
        filter(lambda config: config is not None and config.enabled is True, shops)
    )
    print(f"Found {len(valid_shops)} enabled stores")
    return valid_shops


if __name__ == "__main__":
    load_dotenv()
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
