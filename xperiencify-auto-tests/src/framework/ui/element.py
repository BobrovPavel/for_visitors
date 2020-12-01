from copy import copy

from selenium.webdriver import ActionChains

from src.framework.logger import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from src.framework.ui.browser import Browser

logger = logger.get_logger(log_module=True)


class Element(Browser):

    def __init__(self, driver: WebDriver, *locator):
        super().__init__(driver)
        self.driver = driver
        self.locator = locator

    def as_list(self):
        return self.driver.find_elements(*self.locator)

    def click(self):
        logger.info("Click on [%s]" % str(self.locator))
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable(self.locator)).click()
        return self

    def clear(self):
        logger.info("Clear form [%s]" % str(self.locator))
        self.driver.find_element(*self.locator).clear()
        return self

    def get_attribute(self, attribute):
        return self.driver.find_element(*self.locator).get_attribute(attribute)

    def get_text(self):
        logger.info(f"Getting element text: {self}")
        return self.driver.find_element(*self.locator).text

    def is_displayed(self):
        try:
            return self.driver.find_element(*self.locator).is_displayed()
        except NoSuchElementException:
            return False

    def is_clickable(self):
        try:
            WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable(self.locator))
            return True
        except TimeoutException:
            return False

    def is_enabled(self):
        return self.driver.find_element(*self.locator).is_enabled()

    def is_selected(self):
        return self.driver.find_element(*self.locator).is_selected()

    def is_empty(self):
        return False if self.get_attribute("value") else True

    def type_value(self, value):
        logger.info("Type text '%s' in %s" % (value, self.locator))
        element = self.driver.find_element(*self.locator)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable(self.locator))
        element.clear()
        element.send_keys(value)
        return self

    def safe_type_value(self, value):
        element = self.driver.find_element(*self.locator)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable(self.locator))
        element.clear()
        for i in value:
            element.send_keys(i)
        return self

    def wait_for_visibility(self):
        WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located(self.locator))
        return self
