from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from buyers.base_buyer import BaseBuyer
from buyers.models.credit_card import CreditCard


class SmythsIreBuyer(BaseBuyer):
    def __init__(self, driver: ChromeDriver):
        super().__init__(
            driver,
            "https://www.smythstoys.com/ie/en-ie/video-games-and-tablets/playstation-4/playstation-4-accessories/stealth-playstation-4-play-and-charge-dock/p/180333",
        )

    def buy(self, credit_card: CreditCard):
        self._driver.implicitly_wait(30)

        self._accept_cookies()
        self._login()
        self._add_to_cart()
        self._pay(credit_card)

    def _accept_cookies(self):
        self._driver.get("https://www.smythstoys.com/ie/en-ie")
        self._driver.find_element_by_class_name("cookie-btn-yes").click()
        WebDriverWait(self._driver, 30).until(
            cookie_has_loaded("smyths_gtm_GOOGLEADWORDS", "true")
        )
        print("Cookies accepted")

    def _login(self):
        self._driver.get("https://www.smythstoys.com/ie/en-ie/login")
        self._driver.find_element_by_id("j_username").send_keys(
            os.getenv("SMYTHS_USERNAME")
        )
        self._driver.find_element_by_id("j_password").send_keys(
            os.getenv("SMYTHS_PASSWORD")
        )
        self._driver.find_element_by_id("loginSubmit").click()
        print("Logged in")

    def _add_to_cart(self):
        self._driver.get(self._ps5_page_url)
        self._driver.find_element_by_id("addToCartButton").click()
        print("Added to cart")

    def _pay(self, credit_card):
        self._driver.get(
            "https://www.smythstoys.com/ie/en-ie/checkout/multi/delivery-address/add"
        )
        self._driver.find_element_by_id("addressSubmit").click()
        self._driver.find_element_by_id("deliveryMethodSubmit").click()
        print("Shipping info entered")

        self._driver.find_element_by_id("cardNumberPart1").send_keys(credit_card.number)

        self._driver.find_element_by_css_selector("[data-id='expiryMonth']").click()
        self._driver.find_element_by_css_selector(
            f"[rel='{credit_card.expiration_month}']"
        ).click()

        self._driver.find_element_by_css_selector("[data-id='expiryYear']").click()
        self._driver.find_elements_by_css_selector(
            f"[rel='{credit_card.expiration_year-2020}']"
        )[1].click()
        self._driver.find_element_by_id("cardCvn").send_keys(credit_card.cvv)
        self._driver.find_elements_by_class_name("control__indicator")[1].click()
        print("Purchased")


class cookie_has_loaded:
    """An expectation for checking that a cookie has loaded and has the desired value."""

    def __init__(self, cookie, desired_value):
        self._cookie = cookie
        self._desired_value = desired_value

    def __call__(self, driver: ChromeDriver):
        cookie = driver.get_cookie(self._cookie)
        if cookie and cookie["value"] == self._desired_value:
            return True
        else:
            return False
