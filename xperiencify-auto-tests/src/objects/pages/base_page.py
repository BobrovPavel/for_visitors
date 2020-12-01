from src.framework.ui.brower import Browser
from selenium.webdriver.chrome.webdriver import WebDriver


class BasePage(Browser):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
