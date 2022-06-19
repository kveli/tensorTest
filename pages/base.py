from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver, url="https://yandex.ru"):
        self.driver = driver
        self.url = url

    def get(self):
        return self.driver.get(self.url)

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time)\
            .until(expected_conditions.presence_of_element_located(locator))

    def find_and_click_element(self, locator):
        self.find_element(locator).click()

    def get_screenshot_as_png(self):
        return self.driver.get_screenshot_as_png()

    def save_screenshot(self, file_name: str):
        return self.driver.save_screenshot(file_name)
