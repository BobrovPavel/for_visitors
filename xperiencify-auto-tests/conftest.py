import pytest
from src.framework.logger import logger
from src.objects.users.students import Students
from src.framework.application.application import Application

fixture = None
students = Students()


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--server", action="store", default="dev")


@pytest.fixture(scope="session", autouse=True)
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    fixture = Application(browser)
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    request.addfinalizer(fixture.destroy)
    return fixture


@pytest.fixture(scope="function")
def refresh_page():
    yield
    fixture.driver.refresh()


@pytest.fixture(scope="session", autouse=True)
def get_server(request):
    pytest.server_domain = request.config.getoption("--server")
    return request.config.getoption("--server")


@pytest.fixture(scope="session")
def choice_server(get_server):
    def get_url(subdomain=None, slug=None):
        if subdomain and slug:
            return f"https://{subdomain}.xperiencify.{get_server}/{slug}/"
        elif subdomain:
            return f"https://{subdomain}.xperiencify.{get_server}/"
        elif slug:
            return f"https://xperiencify.{get_server}/{slug}/"
        else:
            return f"https://xperiencify.{get_server}/"

    return get_url


@pytest.fixture(scope="function", autouse=True)
def log_module(request):
    """
    add test function name to log file
    do not forget to set the flag again in True
    to return the full log format for logging
    """
    test_name_logger = logger.get_logger(log_module=False)
    test_name_logger.info(f">>> \tStart test {request.node.name.upper()}")
    logger.get_logger(log_module=True)

# def pytest_runtest_call(item):
#     """
#     add test function name to log file
#     do not forget to set the flag again in True
#     to return the full log format for logging
#     """
#     test_name_logger = logger.get_logger(log_module=False)
#     test_name_logger.info(f">>> \tStart test {item}")
#     logger.get_logger(log_module=True)
