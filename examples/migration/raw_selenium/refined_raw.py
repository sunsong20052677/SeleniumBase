"""Refined Raw Selenium Example - (This test does NOT use SeleniumBase)"""
import sys
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from unittest import TestCase


class RefinedRawSelenium(TestCase):
    def setUp(self):
        self.driver = None
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        if "linux" in sys.platform:
            options.add_argument("--headless")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"],
        )
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        if self.driver:
            try:
                if self.driver.service.process:
                    self.driver.quit()
            except Exception:
                pass

    def wait_for_element_visible(
        self, selector, by="css selector", timeout=10
    ):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, selector))
        )

    def wait_for_element_clickable(
        self, selector, by="css selector", timeout=10
    ):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, selector))
        )

    def wait_for_element_not_visible(
        self, selector, by="css selector", timeout=10
    ):
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element((by, selector))
        )

    def open(self, url):
        self.driver.get(url)

    def click(self, selector, by="css selector", timeout=7):
        el = self.wait_for_element_clickable(selector, by=by, timeout=timeout)
        el.click()

    def type(self, selector, text, by="css selector", timeout=10):
        el = self.wait_for_element_clickable(selector, by=by, timeout=timeout)
        el.clear()
        if not text.endswith("\n"):
            el.send_keys(text)
        else:
            el.send_keys(text[:-1])
            el.submit()

    def assert_element(self, selector, by="css selector", timeout=7):
        self.wait_for_element_visible(selector, by=by, timeout=timeout)

    def assert_text(self, text, selector="html", by="css selector", timeout=7):
        el = self.wait_for_element_visible(selector, by=by, timeout=timeout)
        self.assertIn(text, el.text)

    def assert_exact_text(self, text, selector, by="css selector", timeout=7):
        el = self.wait_for_element_visible(selector, by=by, timeout=timeout)
        self.assertEqual(text, el.text)

    def assert_element_not_visible(
        self, selector, by="css selector", timeout=7
    ):
        self.wait_for_element_not_visible(selector, by=by, timeout=timeout)

    def test_add_item_to_cart(self):
        self.open("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce\n")
        self.assert_element("div.inventory_list")
        self.assert_text("PRODUCTS", "span.title")
        self.click('button[name*="backpack"]')
        self.click("#shopping_cart_container a")
        self.assert_exact_text("YOUR CART", "span.title")
        self.assert_text("Backpack", "div.cart_item")
        self.click("#remove-sauce-labs-backpack")
        self.assert_element_not_visible("div.cart_item")
        self.click("#react-burger-menu-btn")
        self.click("a#logout_sidebar_link")
        self.assert_element("input#login-button")
