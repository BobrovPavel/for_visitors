import time

BASE_WAIT = 4
SHORT_WAIT = 2
REQUEST_TIME_LIMIT = 10

visa_default_number = "4242424242424242"
zip_default = "55555"
cvc_default = "123"
first_name_default = "First"
last_name_default = "Last"
email_default = "email@gmail.com"
email_without_at = "emailgmail.com"
email_without_domain = "email@gmail"
email_with_special_characters = "%^Y&U@gmail.com"
business_default = "Business"
phone_default = "123456789"
empty_field = ""
password_default = "DEFAULTpassword123"


def unique_email():
    return f"{str(time.time())}@gmail.com"

def unique_name():
    return f"First{str(int(time.time()))}"

ORDER_FORM_API_KEY = ""
