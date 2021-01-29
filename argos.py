import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

hue_api_user = os.getenv("HUE_API_USER")
while True:
    response = requests.get("https://www.argos.ie/static/Browse/ID72/50002742/c_1/1%7Ccategory_root%7CVideo+games%7C14419738/c_2/2%7Ccat_14419738%7CPS5%7C50002742.htm")
    if response.ok:
        html = BeautifulSoup(response.text, "html.parser")
        if html.find('a', title="The Playstation 5 is out of stock.") is None:
            print("PS5 potentially live on Argos!!")
            print(requests.put(f"http://192.168.0.100/api/{hue_api_user}/groups/1/action", json={ "alert": "lselect", "bri": 254 }).json)
            print(requests.put(f"http://192.168.0.100/api/{hue_api_user}/groups/2/action", json={ "alert": "lselect", "bri": 254 }).json)
            break
        else:
            print("No PS5s found")
            time.sleep(60)
    else:
        print(f"Argos returned bad response status: {response}")
        break
print("Exiting")
