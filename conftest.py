import pytest
from selenium import webdriver

@pytest.fixture()
def chrome_browser():
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(75)
    yield driver
    driver.quit()