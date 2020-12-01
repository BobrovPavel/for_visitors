from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from src.framework.ui.element import Element
from src.objects.pages.base_page import BasePage
from selenium.webdriver.chrome.webdriver import WebDriver
from src.objects.users.students import Students

students = Students()


class OrderPage(BasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)

        self.learn_more_button = Element(self.driver, By.XPATH, "//a[text()='Learn More']")
        self.first_name_input = Element(self.driver, By.XPATH, "//input[@id='user_first_name']")
        self.last_name_input = Element(self.driver, By.XPATH, "//input[@id='user_last_name']")
        self.email_input = Element(self.driver, By.XPATH, "//input[@id='user_email']")
        self.card_number_iframe = Element(self.driver, By.XPATH, "//iframe[@name='__privateStripeFrame5']")
        self.card_number_input = Element(self.driver, By.XPATH, "//input[@name='cardnumber']")
        self.card_date_iframe = Element(self.driver, By.XPATH, "//iframe[@name='__privateStripeFrame6']")
        self.card_date_input = Element(self.driver, By.XPATH, "//input[@name='exp-date']")
        self.card_cvc_iframe = Element(self.driver, By.XPATH, "//iframe[@name='__privateStripeFrame7']")
        self.card_cvc_input = Element(self.driver, By.XPATH, "//input[@name='cvc']")
        self.country_select = Element(self.driver, By.XPATH, "//div[@class='address-fields']//ul")
        self.zip_code_iframe = Element(self.driver, By.XPATH, "//iframe[@name='__privateStripeFrame8']")
        self.zip_code_input = Element(self.driver, By.XPATH, "//input[@name='postal']")
        self.terms_conditions_checkbox = Element(self.driver, By.XPATH, "//label[@id='terms-conditions']")
        self.submit_button = Element(self.driver, By.XPATH, "//button[@class='submit-btn']")

    def get_error_message_text(self, error_locator):
        try:
            return Element(self.driver, By.XPATH, error_locator).get_text()
        except NoSuchElementException:
            return "NoSuchElementException"

    def is_validation_message_displayed(self, error_text, error_locator):
        """
        Compares a constant with web element text
        :param error_text: String constant
        :param error_locator: Locator where the webelement with error is located
        """
        try:
            Element(self.driver, By.XPATH, error_locator).wait_for_visibility()
            result = error_text in self.get_error_message_text(error_locator)
        except TimeoutException:
            return False
        return result

    def is_student_created(self, subdomain, email, *, api_key, server):
        return True if email in students.get_detail(subdomain, email, api_key=api_key, server=server).values() else False

    def is_submit_form_button_clickable(self):
        return self.submit_button.is_clickable()

    def fill_form(self, data, email=None, check=True):
        """
        :param data: Dictionary with test data to fill out the form
        :param email: The email address with which need to create a student
        By default, email is taken from the dictionary
        :param check: Check Terms&Conditions if True and not if False
        """
        self.first_name_input.type_value(data["fname"])
        self.last_name_input.type_value(data["lname"])
        if email:
            self.email_input.type_value(email)
        else:
            self.email_input.type_value(data["email"])
        self.switch_to_frame(self.card_number_iframe.locator)
        self.card_number_input.safe_type_value(data["card_number"])
        self.switch_to_default_content()
        self.switch_to_frame(self.card_date_iframe.locator)
        self.card_date_input.type_value(data["card_date"])
        self.switch_to_default_content()
        self.switch_to_frame(self.card_cvc_iframe.locator)
        self.card_cvc_input.type_value(data["cvc"])
        self.switch_to_default_content()
        self.switch_to_frame(self.zip_code_iframe.locator)
        self.zip_code_input.type_value(data["zip"])
        self.switch_to_default_content()
        if check:
            self.terms_conditions_checkbox.click()
            self.submit_button.click()
