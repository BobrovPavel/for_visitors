import time
from src.commons import constants
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

from src.framework.logger import logger

logger = logger.get_logger()


class Browser:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, constants.BASE_WAIT)
        self.driver.implicitly_wait(3)
        self.action = ActionChains(self.driver)

    def accept_alert(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
        except TimeoutException:
            logger.info("No alert")

    def add_class(self, locator, class_name):
        logger.info("Add [%s] class to element [%s]" % (locator, class_name))
        time.sleep(1.5)  # Wait for execute all jquery requests after click on element
        self.driver.execute_script("return document.querySelector('%s').classList.add('%s')" % (locator, class_name))

    def close_current_tab(self):
        self.driver.close()

    def close_unused_tabs(self):
        number_of_tabs = len(self.driver.window_handles)
        while number_of_tabs > 1:
            self.switch_tab(number_of_tabs - 1)
            self.close_current_tab()
            number_of_tabs = len(self.driver.window_handles)
        self.switch_tab(0)

    def dismiss_alert(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            self.driver.switch_to.alert.dismiss()
        except TimeoutException:
            logger.info("No alert")

    def delete_all_cookies(self):
        self.driver.delete_all_cookies()

    def delete_cookies_and_refresh_page(self):
        self.driver.delete_all_cookies()
        self.driver.refresh()

    def get_current_url(self):
        return self.driver.current_url

    def get_page_title(self):
        return self.driver.title

    def go_to_first_tab(self):
        if len(self.driver.window_handles) > 1:
            self.close_current_tab()
            self.switch_tab(0)

    def is_alert_present(self):
        try:
            alert = self.driver.switch_to.alert
            logger.info("Alert is present [%s]" % alert)
            return True
        except NoAlertPresentException:
            logger.info("No alert")
            return False

    def open(self, url):
        logger.info("Open page: %s" % url)
        self.driver.get(url)

    def refresh_page(self):
        logger.info("Refresh page")
        self.driver.refresh()
        while self.is_alert_present():
            self.driver.switch_to.alert.dismiss()
            self.driver.refresh()
            time.sleep(.3)

    def scroll_to_top_page(self):
        logger.info("Scroll to top page")
        self.action.send_keys_to_element(self.driver.find_element_by_tag_name('body'), Keys.CONTROL + Keys.HOME).perform()

    def send_escape(self):
        self.action.send_keys(Keys.ESCAPE).perform()

    def send_enter(self):
        self.action.send_keys(Keys.RETURN).perform()

    def send_key(self, key):
        action = ActionChains(self.driver)
        action.send_keys(key).perform()

    def switch_to_frame(self, locator):
        self.driver.switch_to.frame(self.driver.find_element(*locator))

    def switch_to_default_content(self):
        logger.info("Switch to default content")
        self.driver.switch_to.default_content()

    def switch_tab(self, tab_number):
        logger.info(f"Switch to {tab_number} tab")
        self.driver.switch_to.window(self.driver.window_handles[tab_number])
