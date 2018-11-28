from SupportLibraries.driver_factory import DriverFactory
import pytest


@pytest.fixture(scope="session")
def get_driver(request, platform):
    print("session_level_setup: Running session level setup.")
    df = DriverFactory(platform)
    driver = df.get_driver_instance()
    driver.reset()
    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "driver", driver)
    yield
    print("session_level_setup: Running session level teardown.")
    driver.reset()

def pytest_addoption(parser):
    parser.addoption("--platform", help="Mobile Platform")


@pytest.fixture(scope="session")
def platform(request):
    return request.config.getoption("--platform")
