from allure_commons.types import AttachmentType

from pages.search import SearchPage
from selenium import webdriver
import allure

from tests.report import allure_screenshot

driver: webdriver

@allure.feature('Yandex search')
@allure.story('1. Проверяем наличие поля ввода')
def test_check_form_search(start_driver):
    global driver
    driver = SearchPage(start_driver)
    driver.get()
    search_input_check = driver.search_input()
    allure_screenshot(driver, 'test_check_form_search')
    assert search_input_check is not None

@allure.feature('Yandex search')
@allure.story('2. Проверяем появление окна подсказок')
def test_suggest_is_displayed():
    suggest = driver.open_suggest('Тензор')
    allure_screenshot(driver, 'test_suggest_is_displayed')
    assert suggest.is_displayed() is True

@allure.feature('Yandex search')
@allure.story('3. Проверяем первую ссылку в результатах поиска')
def test_first_url():
    host = driver.check_link().get_attribute('host')
    allure_screenshot(driver, 'test_first_url')
    assert host == "tensor.ru"
