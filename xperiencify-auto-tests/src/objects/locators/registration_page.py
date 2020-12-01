from selenium.webdriver.common.by import By
from src.framework.ui.locator import Locator


class StudentRegistrationPageLocators:
    create_an_account_link = Locator(By.XPATH, "//button[contains(text(),'Create')]")
    student_registration_form = Locator(By.XPATH, "//form[@class='signin']")
    first_name_input = Locator(By.XPATH, "//input[@name='first_name']")
    last_name_input = Locator(By.XPATH, "//input[@name='last_name']")
    email_input = Locator(By.XPATH, "//input[@name='email']")
    password_input = Locator(By.XPATH, "//input[@name='password1']")
    confirm_password_input = Locator(By.XPATH, "//input[@name='password2']")
    sign_up_button = Locator(By.XPATH, "//button[@name='signin']")
    field_error_class = Locator(By.XPATH, "//div[@class='field']")
