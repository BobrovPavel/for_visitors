from src.objects.locators.registration_page import StudentRegistrationPageLocators as student_locators

student_invalid_data = [
    {
        "test_name": "without_fname",
        "fname": "",
        "lname": "Last",
        "locator": student_locators.first_name_input.locator,
        "error_message": "This field is required"
    },
    {
        "test_name": "without_lname",
        "fname": "First",
        "lname": "",
        "locator": student_locators.last_name_input.locator,
        "error_message": "This field is required"
    },
    {
        "test_name": "without_email",
        "fname": "First",
        "lname": "Last",
        "locator": student_locators.email_input.locator,
        "error_message": "This field is required"
    },
    {
        "test_name": "without_confirm_password",
        "fname": "First",
        "lname": "Last",
        "locator": student_locators.confirm_password_input.locator,
        "error_message": "This field is required"
    },
    {
        "test_name": "with_different_passwords",
        "fname": "First",
        "lname": "Last",
        "locator": student_locators.field_error_class.locator,
        "error_message": "The two password fields didn't match"
    },
    {
        "test_name": "with_less_than_8_chars_password",
        "fname": "First",
        "lname": "Last",
        "locator": student_locators.password_input.locator,
        "error_message": "This password is too short. It must contain at least 8 characters"
    },
    {
        "test_name": "with_only_numbers_password",
        "fname": "First",
        "lname": "Last",
        "locator": student_locators.password_input.locator,
        "error_message": "This password is too common"
    },
    {
        "test_name": "with_existing_email",
        "fname": "First",
        "lname": "Last",
        "locator": student_locators.email_input.locator,
        "error_message": "Email is already in use"
    },
    {
        "test_name": "with_existing_email_in_camel_case",
        "fname": "First",
        "lname": "Last",
        "locator": student_locators.email_input.locator,
        "error_message": "Email is already in use"
    }
]