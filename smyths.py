import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

hue_api_user = os.getenv("HUE_API_USER")
while True:
    response = requests.get("https://www.smythstoys.com/ie/en-ie/video-games-and-tablets/playstation-5/playstation-5-consoles/playstation-5-console/p/191259")
    if response.ok:
        html = BeautifulSoup(response.text, "html.parser")
        if html.find('td', string="Out of Stock. Expected in stock: January 2021") is None:
            print("PS5 potentially live on Smyths!!")
            print(requests.put(f"http://192.168.0.100/api/{hue_api_user}/groups/1/action", json={ "alert": "lselect", "bri": 254 }).json)
            print(requests.put(f"http://192.168.0.100/api/{hue_api_user}/groups/2/action", json={ "alert": "lselect", "bri": 254 }).json)
            break
        else:
            print("No PS5s found on smyths")
            time.sleep(60)
    else:
        print(f"Smyths returned bad response status: {response}")
        break
print("Exiting")
