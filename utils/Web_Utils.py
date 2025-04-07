import time
import logging

import allure
from selenium.common.exceptions import (
    ElementClickInterceptedException, NoSuchElementException,
    ElementNotInteractableException, TimeoutException)
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebUtils:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)
        self.logger = logging.getLogger(self.__class__.__name__)

    def click_on_element(self, locator):
        """Click an element, using JavaScript if it's intercepted."""
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
            self.logger.info(f"Clicked element: {locator}")
            with allure.step(f"Clicked element: {locator}"):
                pass
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(*locator))
            self.logger.info(f"Clicked element using JavaScript: {locator}")
            with allure.step(f"Clicked element using JavaScript: {locator}"):
                pass
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"Error clicking element {locator}: {e}")
            with allure.step(f"Error clicking element {locator}: {e}"):
                pass

    def enter_text_in_field(self, locator, value):
        """Clear and enter text in an input field, using JavaScript if necessary."""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            element.clear()
            element.send_keys(value)
            self.logger.info(f"Entered text in element {locator}: {value}")
            with allure.step(f"Entered text: {value} in element {locator}"):
                pass
        except ElementNotInteractableException:
            self.driver.execute_script("arguments[0].value = arguments[1];", self.driver.find_element(*locator), value)
            self.logger.info(f"Set text using JavaScript in element {locator}: {value}")
            with allure.step(f"Set text using JavaScript in element {locator}: {value}"):
                pass
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"Error entering text for element {locator}: {e}")
            with allure.step(f"Error entering text for element {locator}: {e}"):
                pass

    def is_element_visible(self, locator):
        """Check if an element is visible on the page."""
        try:
            visible = self.wait.until(EC.presence_of_element_located(locator)).is_displayed()
            self.logger.info(f"Element {locator} visibility: {visible}")
            allure.attach(self.driver.get_screenshot_as_png(), name=f"Element: {locator} is visible", attachment_type=allure.attachment_type.PNG)
            return visible
        except (NoSuchElementException, TimeoutException):
            self.logger.info(f"Element {locator} is not visible.")
            allure.attach(self.driver.get_screenshot_as_png(), name=f"Element: {locator} is not visible", attachment_type=allure.attachment_type.PNG)
            return False

    def wait_until_element_is_visible(self, locator, timeout=10):
        """Wait until an element becomes visible."""
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            self.logger.info(f"Element {locator} is now visible.")
            return element
        except TimeoutException:
            self.logger.error(f"Timeout: Element {locator} not visible.")
            return None

    def scroll_to_web_element(self, locator):
        """Scroll to a specific web element."""
        try:
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.logger.info(f"Scrolled to element {locator}.")
        except NoSuchElementException:
            self.logger.error(f"Element {locator} not found for scrolling.")

    def get_text_from_element(self, locator):
        """Retrieve text content from an element."""
        try:
            text = self.wait.until(EC.presence_of_element_located(locator)).text.strip()
            self.logger.info(f"Retrieved text from element {locator}: {text}")
            return text
        except (NoSuchElementException, TimeoutException):
            self.logger.error(f"Text not found for element {locator}.")
            return ""

    def navigate_back_to_previous_page(self):
        """Navigate back to the previous page in browser history."""
        self.driver.back()
        self.logger.info("Navigated back to the previous page.")

    def select_by_visible_text(self, locator, text):
        """Select an option from a dropdown by visible text."""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            Select(element).select_by_visible_text(text)
            self.logger.info(f"Selected option '{text}' from dropdown {locator}")
            with allure.step(f"Selected option '{text}' from dropdown {locator}"):
                pass
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"Error selecting option '{text}' from dropdown {locator}: {e}")
            with allure.step(f"Error selecting option '{text}' from dropdown {locator}: {e}"):
                pass

    def select_by_value(self, locator, value):
        """Select an option from a dropdown by value."""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            Select(element).select_by_value(value)
            self.logger.info(f"Selected option with value '{value}' from dropdown {locator}")
            with allure.step(f"Selected option with value '{value}' from dropdown {locator}"):
                pass
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"Error selecting option with value '{value}' from dropdown {locator}: {e}")
            with allure.step(f"Error selecting option with value '{value}' from dropdown {locator}: {e}"):
                pass

    def select_by_index(self, locator, index):
        """Select the dropdown option based on the index from dropdown."""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            Select(element).select_by_index(index)
            self.logger.info(f"Selected option with index '{index}' from dropdown {locator}")
            with allure.step(f"Selected option with index '{index}' from dropdown {locator}"):
                pass
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"Error selecting option with index '{index}' from dropdown {locator}: {e}")
            with allure.step(f"Error selecting option with index '{index}' from dropdown {locator}: {e}"):
                pass

    def get_values_from_the_dropdown(self, locator):
        """
        Retrieve all visible option values from a dropdown element.
        :param locator: Tuple representing the dropdown locator (By, value)
        :return: List of visible option texts
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            select = Select(element)
            options = [opt.text.strip() for opt in select.options]
            return options
        except (NoSuchElementException, TimeoutException) as e:
            return []
