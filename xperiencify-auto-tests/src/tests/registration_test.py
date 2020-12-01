import pytest
from src.framework.logger import logger
from src.objects.data.coach_registration_data import *
from src.objects.data.student_registration_data import *


logger = logger.get_logger()


@pytest.fixture(scope="class")
def open_subdomain_form(app, choice_server):
    app.browser.open(choice_server(slug="registration"))
    app.coach_registration.fill_form(coach_default_data)
    app.coach_registration.submit_form()


@pytest.fixture(scope="function")
def open_registration_page(app, choice_server):
    app.browser.open(choice_server(slug="registration"))


@pytest.fixture(scope="function")
def open_registration_form(app, choice_server):
    app.browser.open(choice_server(slug="login"))
    app.student_registration.open_registration_form()


@pytest.mark.usefixtures("open_registration_page")
class TestRegistration:

    @pytest.mark.parametrize("data", coach_invalid_data)
    def test_coach_registration_with_invalid_data(self, app, data):
        logger.info(f"Test coach registration: {data['test_name']}")
        app.coach_registration.fill_form(data)
        app.coach_registration.submit_form()
        assert app.coach_registration.is_validation_message_displayed(), "Error message isn't displayed"

    @pytest.mark.parametrize("data", coach_valid_data)
    def test_coach_registration_with_valid_data(self, app, data):
        logger.info(f"Test coach registration: {data['test_name']}")
        app.coach_registration.fill_form(data)
        app.coach_registration.submit_form()
        assert app.coach_registration.is_next_registration_step_open(), "Subdomain form was not open"

    def test_expire_date_list_not_have_past_years(self, app):
        assert app.coach_registration.is_not_past_year_in_years_list(current_year=current_year), "Years list have current year"

    def test_user_cannot_submit_form_without_accept_terms_and_conditions(self, app):
        app.coach_registration.fill_form(coach_default_data)
        app.coach_registration.uncheck_terms_and_conditions()
        app.coach_registration.submit_form()
        assert not app.coach_registration.is_next_registration_step_open(), "Subdomain form is open without terms & conditions confirmation"

    def test_open_terms_and_conditions_page(self, app):
        app.coach_registration.open_terms_and_conditions_page()
        assert app.coach_registration.is_terms_and_conditions_page_open(), "Wrong selector or page was not open"

    def test_email_field_have_browser_validation(self, app):
        assert app.coach_registration.is_email_field_have_email_type(), "Field have not email type"


@pytest.mark.usefixtures("open_subdomain_form")
@pytest.mark.usefixtures("refresh_page")
class TestSubdomain:

    def test_sub_domain_field_is_empty_by_default(self, app):
        app.coach_registration.subdomain_input.wait_for_visibility()
        assert app.coach_registration.confirm_subdomain_button.is_empty(), "Domain field is not empty"

    def test_subdomain_field_is_required(self, app):
        app.coach_registration.subdomain_input.wait_for_visibility().type_value(unique_subdomain).clear()
        pytest.assume(app.coach_registration.is_validation_message_displayed(), "Error message isn't displayed")
        pytest.assume(not app.coach_registration.confirm_subdomain_button.is_clickable(), "Button is clickable")

    def test_subdomain_special_characters_validation(self, app):
        app.coach_registration.subdomain_input.wait_for_visibility().type_value(special_characters_subdomain)
        pytest.assume(not app.coach_registration.is_special_chars_in_subdomain(special_characters_subdomain), "Special characters aren't replaced")
        pytest.assume(not app.coach_registration.confirm_subdomain_button.is_clickable(), "Button is clickable")

    def test_existing_subdomain(self, app):
        """
        Make sure the domain is already taken
        """
        app.coach_registration.subdomain_input.wait_for_visibility().type_value(existing_subdomain)
        pytest.assume(app.coach_registration.is_validation_message_displayed()), "Validation message is not displayed"
        pytest.assume(not app.coach_registration.confirm_subdomain_button.is_clickable(), "Button is clickable")

    def test_subdomain_less_than_min_len(self, app):
        app.coach_registration.subdomain_input.wait_for_visibility().type_value(four_characters_subdomain)
        pytest.assume(app.coach_registration.is_validation_message_displayed()), "Validation message is not displayed"
        pytest.assume(not app.coach_registration.confirm_subdomain_button.is_clickable(), "Button is clickable")

    def test_subdomain_equal_min_len(self, app):
        app.coach_registration.subdomain_input.wait_for_visibility().type_value(five_characters_subdomain)
        pytest.assume(not app.coach_registration.is_validation_message_displayed()), "Validation message is not displayed"
        pytest.assume(app.coach_registration.confirm_subdomain_button.is_clickable(), "Button isn't clickable")


@pytest.mark.usefixtures("open_registration_form")
class TestStudentRegistration:

    @pytest.mark.parametrize("data", student_invalid_data)
    def test_student_reg_with_invalid_data(self, app, data):
        logger.info(f"Test student registration: {data['test_name']}")
        app.student_registration.fill_form(data)
        assert app.student_registration.is_validation_message_displayed(data["locator"], data["error_message"]), \
            f"\nError message is not displayed or incorrect text " \
            f"\nExpected: {data['error_message']} " \
            f"\nActual: {app.student_registration.get_error_message_text(data['locator'])}"
