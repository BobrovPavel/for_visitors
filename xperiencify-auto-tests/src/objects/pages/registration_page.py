from selenium.webdriver.common.by import By
from src.framework.ui.element import Element
from src.objects.pages.base_page import BasePage
from src.objects.locators.registration_page import StudentRegistrationPageLocators


class CoachRegistrationPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.coach_first_name_input = Element(self.driver, By.XPATH, "//input[@name='general-first_name']")
        self.coach_last_name_input = Element(self.driver, By.XPATH, "//input[@name='general-last_name']")
        self.coach_email_input = Element(self.driver, By.XPATH, "//input[@name='general-email']")
        self.coach_company_input = Element(self.driver, By.XPATH, "//input[@name='general-company']")
        self.coach_phone_input = Element(self.driver, By.XPATH, "//input[@name='general-phone']")
        self.coach_card_number_input = Element(self.driver, By.XPATH, "//input[@name='general-card_number']")
        self.coach_cvc_input = Element(self.driver, By.XPATH, "//input[@name='general-card_cvc']")
        self.coach_card_year_droplist_arrow_icon = Element(self.driver, By.XPATH, "//ul[@data-input='general-card_exp_year']//*[@class='icon']")
        self.terms_and_conditions_checkbox = Element(self.driver, By.XPATH, "//*[@class='check__box']")
        self.terms_and_conditions_check_input = Element(self.driver, By.XPATH, "//input[@class='check__input']")
        self.terms_and_conditions_link = Element(self.driver, By.XPATH, "//a[contains(.,'conditions')]")
        self.create_your_account_button = Element(self.driver, By.XPATH, "//button[@type='submit']")
        self.validation_message = Element(self.driver, By.XPATH, "//p[@class='validation-message']")
        self.card_type_droplist = Element(self.driver, By.XPATH, "//label[contains(text(),'Card type')]//ul")
        self.selected_card_type = Element(self.driver, By.XPATH, "//label[contains(text(),'Card type')]//li[contains(@class,'selected')]")
        self.coach_site_name_input = Element(self.driver, By.XPATH, "//input[@id='registration-site-name']")
        self.coach_card_year_item = Element(self.driver, By.XPATH, "//ul[@data-input='general-card_exp_year']//li[contains(@class,'select-item')]")
        self.subdomain_input = Element(self.driver, By.XPATH, "//input[@id='registration-site-name']")
        self.confirm_subdomain_button = Element(self.driver, By.XPATH, "//form[@data-validate-url='/validate_subdomain']//button")

    def fill_form(self, data):
        self.coach_first_name_input.type_value(data["fname"])
        self.coach_last_name_input.type_value(data["lname"])
        self.coach_email_input.type_value(data["email"])
        self.coach_company_input.type_value(data["business"])
        self.coach_phone_input.type_value(data["phone"])
        self.select_card_type(data["card_type"])
        self.coach_card_number_input.type_value(data["card_number"])
        self.coach_cvc_input.type_value(data["cvc"])
        self.select_year(data["year"])
        self.terms_and_conditions_checkbox.click()

    def select_year(self, year):
        self.coach_card_year_droplist_arrow_icon.click()
        Element(self.driver, By.XPATH, f"//li[@data-value='{year}']").click()

    def select_card_type(self, card_type):
        if self.selected_card_type.get_text() not in card_type:
            self.card_type_droplist.click()
            Element(self.driver, By.XPATH, f"//li[contains(@class,'select-item')][contains(text(),'{card_type}')]").click()

    def submit_form(self):
        self.create_your_account_button.click()

    def is_next_registration_step_open(self):
        return self.coach_site_name_input.is_displayed()

    def is_email_field_have_email_type(self):
        return self.coach_email_input.get_attribute("type") == "email"

    def is_validation_message_displayed(self):
        return self.validation_message.is_displayed()

    def is_not_past_year_in_years_list(self, current_year):
        return str(current_year - 1) not in [item.get_attribute("data-value") for item in self.coach_card_year_item.as_list()]

    def is_special_chars_in_subdomain(self, subdomain):
        return True if [i for i in subdomain if i in self.subdomain_input.get_attribute("value")] else False

    def is_terms_and_conditions_page_open(self):
        return "https://howto.xperiencify.com/article.php?article=terms" in self.driver.current_url

    def open_terms_and_conditions_page(self):
        self.terms_and_conditions_link.click()
        self.switch_tab(1)

    def uncheck_terms_and_conditions(self):
        if self.terms_and_conditions_check_input.is_selected():
            self.terms_and_conditions_checkbox.click()


class StudentRegistrationPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = StudentRegistrationPageLocators()

        self.create_an_account_link = Element(self.driver, By.XPATH, "//button[contains(text(),'Create')]")
        self.student_registration_form = Element(self.driver, By.XPATH, "//form[@class='signin']")
        self.first_name_input = Element(self.driver, By.XPATH, "//input[@name='first_name']")
        self.last_name_input = Element(self.driver, By.XPATH, "//input[@name='last_name']")
        self.email_input = Element(self.driver, By.XPATH, "//input[@name='email']")
        self.password_input = Element(self.driver, By.XPATH, "//input[@name='password1']")
        self.confirm_password_input = Element(self.driver, By.XPATH, "//input[@name='password2']")
        self.sign_up_button = Element(self.driver, By.XPATH, "//button[@name='signin']")

    def get_error_message_text(self, locator):
        return Element(self.driver, By.XPATH, f"{locator}//following-sibling::*").get_text()

    def is_validation_message_displayed(self, locator, error):
        """
        :param locator: The locator of the item to check for errors
        :param error: Error text
        :return: Boolean
        """
        return error in self.get_error_message_text(locator)

    def open_registration_form(self):
        self.create_an_account_link.click()
        self.student_registration_form.wait_for_visibility()

    def fill_form(self, data):
        self.first_name_input.type_value(data["fname"])
        self.last_name_input.type_value(data["lname"])
        self.email_input.type_value(data["email"])
        self.password_input.type_value(data["pass1"])
        self.confirm_password_input.type_value(data["pass2"])
        self.sign_up_button.click()
