from selenium import webdriver
from src.framework.ui.brower import Browser
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from src.objects.pages.order_form_page import OrderPage
from src.objects.pages.registration_page import CoachRegistrationPage, StudentRegistrationPage


class Application:

    def __init__(self, browser):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--start-maximized")
        if browser == "chrome":
            self.driver = webdriver.Chrome(options=self.chrome_options)
        elif browser == "firefox":
            self.driver = webdriver.Firefox()
            self.driver.maximize_window()
        self.driver.implicitly_wait(1)
        self.wait = WebDriverWait(self.driver, 45)
        self.browser = Browser(self.driver)
        self.coach_registration = CoachRegistrationPage(self.driver)
        self.student_registration = StudentRegistrationPage(self.driver)
        self.order_form = OrderPage(self.driver)

    def destroy(self):
        self.driver.quit()
