import pytest
from selenium import webdriver


@pytest.fixture(scope="session")
def start_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    driver = webdriver.Chrome(
        executable_path=r"C:\chromedriver.exe",
        options=options
    )
    yield driver
    driver.quit()
