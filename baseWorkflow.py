import os
import time
import requests
import json
from multiprocessing import Process
from bs4 import BeautifulSoup
from models.shop import Shop

CONFIG_DIR = 'configs/'


def run_workflow(store):
    while True:
        check_store(store)
        time.sleep(store.wait_time)

def check_store(store: Shop):
    print(f"Checking store: {store.name} at url: {store.url}")
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}
    response = requests.get(store.url, headers=headers)
    if response.ok:
        html = BeautifulSoup(response.text, "html.parser")
        for out_of_stock_element in store.out_of_stock_elements:
            text_search = html(text=lambda t: out_of_stock_element in t) or []            
            element_search = html.find_all(title=out_of_stock_element)
            full_search_result = text_search + element_search
            if full_search_result:
                print(f"Got {len(full_search_result)} for {store.name} hits: {element_search}")
                return
        print(f"Potential stock available for store: {store.name}")
    else:
        print(f"Store: {store.name} returned bad response status: {response}")

def get_stores():
    shops = []
    configs = os.listdir(CONFIG_DIR)
    print(f"Found {len(configs)} configs")
    for store_config in configs:
        with open(f"{CONFIG_DIR}{store_config}") as json_file:
            raw_config = json.load(json_file)
            shops.append(Shop(**raw_config))
    valid_shops = list(filter(lambda config : config.enabled is True ,shops))
    print(f"Found {len(valid_shops)} enabled stores")
    return valid_shops

if __name__ == '__main__':
    processes = []
    for store in get_stores():
        p = Process(target=run_workflow, args=(store,))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()
