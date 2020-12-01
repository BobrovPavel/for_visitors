import pytest
from src.framework.logger import logger
from src.objects.payments.stripe import Stripe
from src.objects.users.students import Students
from src.commons.constants import unique_email, unique_name, email_default, ORDER_FORM_API_KEY
from src.objects.data.order_page_data import order_invalid_data, order_valid_data, order_default_data

logger = logger.get_logger()
subdomain = "test-order-form"
students = Students()
stripe = Stripe()


@pytest.fixture(scope="function")
def setup(app, choice_server):
    app.browser.open(choice_server(subdomain=subdomain))
    app.order_form.learn_more_button.click()
    app.browser.switch_tab(1)
    yield
    app.browser.close_unused_tabs()
    app.browser.delete_all_cookies()
    app.browser.refresh_page()


@pytest.fixture
def open_order_form(app, choice_server):
    app.browser.open(choice_server(subdomain=subdomain))
    app.order_form.learn_more_button.click()
    app.browser.switch_tab(1)


@pytest.fixture(scope="function", autouse=True)
def clean_up():
    students.delete_all(subdomain, api_key=ORDER_FORM_API_KEY, server=pytest.server_domain)


@pytest.mark.usefixtures("setup")
class TestOrderFormWithInvalidData:
    """
    Preparation:
    1. Configure stripe for coach - https://prnt.sc/reo7zi
    2. Configure Sales Page for program - https://prnt.sc/reo91j
    3. Configure Price for program - https://prnt.sc/reoa6s

    Test Stripe api-keys:
    Publish key - pk_test_kWdgJdvDDF00GyDVs9cdsZU1
    Secret key -  sk_test_EzsGYi9Bh90a0SCFQ1ZtMQOL
    """

    @pytest.mark.parametrize("data", order_invalid_data)
    def test_create_student_with_invalid_data(self, app, data):
        app.order_form.fill_form(data)
        assert app.order_form.is_validation_message_displayed(data["error_message"], data["error_locator"]), \
            f"\nError message is not displayed or incorrect text " \
            f"\nExpected: {data['error_message']} " \
            f"\nActual: {app.order_form.get_error_message_text(data['error_locator'])}"

    def test_user_cannot_submit_form_without_accept_terms_and_conditions(self, app):
        app.order_form.fill_form(*order_default_data, check=False)
        assert not app.order_form.is_submit_form_button_clickable()


@pytest.mark.usefixtures("setup")
class TestOrderFormWithValidData:

    @pytest.mark.parametrize("data", order_valid_data)
    def test_create_student_with_valid_data(self, app, data, email=unique_email()):
        app.order_form.fill_form(data, email)
        students.wait_for_created(subdomain, email, api_key=ORDER_FORM_API_KEY, server=pytest.server_domain)
        assert app.order_form.is_student_created(subdomain, email, api_key=ORDER_FORM_API_KEY, server=pytest.server_domain), "Student is not created"

    def test_student_can_register_with_already_used_email(self, app):
        stripe_balance_before_payment = stripe.get_full_balance()
        students.create(subdomain, email_default, unique_name(), api_key=ORDER_FORM_API_KEY, server=pytest.server_domain)
        app.order_form.fill_form(*order_default_data)
        stripe.wait_for_payment_will_done(stripe.get_full_balance())
        assert stripe_balance_before_payment < stripe.get_full_balance(), "Student is not created or or failed payment"
        assert students.get_assigned_dashboards(subdomain, email_default, api_key=ORDER_FORM_API_KEY, server=pytest.server_domain), "The student was not added to the dashboard after payment"

    def test_create_student_on_production(self, app):
        print(pytest.server_domain)
        # print(students.create("mttest", "QWEQWEQWEQWEQWEQWEQWEQWE@gmail.com"))
