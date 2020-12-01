from selenium.webdriver.common.by import By
from src.framework.ui.locator import Locator


class OrderFormPageLocators:
    first_name_input_error = Locator(By.XPATH, "//div[@id='first-name-errors']")
    last_name_input_error = Locator(By.XPATH, "//div[@id='last-name-errors']")
    email_input_error = Locator(By.XPATH, "//div[@id='email-errors']")
    card_number_input_error = Locator(By.XPATH, "//div[@id='card-errors']")
