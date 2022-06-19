from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from .base import BasePage

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class Locators:
    SEARCH_FIELD = (By.XPATH, ".//form//input[@name='text']")
    SUGGEST_LIST = (By.XPATH, ".//div[contains(@class, 'mini-suggest')]/ul[contains(@id, 'suggest')]")
    FIRST_HREF = (By.XPATH, ".//ul[@id='search-result']/li[@data-cid='0']//a")


class SearchPage(BasePage):
    def search_input(self) -> WebElement:
        """
        Ищет поле поиска на странице

        :return: Возвращает WebElement с локатором SEARCH_FIELD
        """
        return self.find_element(Locators.SEARCH_FIELD)

    def open_suggest(self, query: str, time=5) -> WebElement:
        """
        Заполняет строку поиска переданным значением и ищет таблицу подсказок на странице

        :param query: Поисковый запрос;
        :param time:
        :return: Возвращает WebElement с локатором SUGGEST_LIST
        """
        element = self.search_input()
        element.send_keys(query)
        return WebDriverWait(self.driver, time)\
            .until(expected_conditions.visibility_of_element_located(Locators.SUGGEST_LIST),
                   message=f"Suggest не отобразился")

    def check_link(self) -> WebElement:
        """
        Переходит на страницу с результатами поиска, ищет элемент согласно локатору FIRST_HREF.

        :return: Возвращает первый WebElement из найденных результатов.
        """
        element = self.search_input()
        element.send_keys(Keys.ENTER)
        return self.find_element(Locators.FIRST_HREF)
