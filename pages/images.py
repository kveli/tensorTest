from io import BytesIO

import requests
from PIL import Image
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from . import search
from .base import BasePage

from selenium.webdriver.common.by import By


class Locators:
    SEARCH_FIELD = search.Locators.SEARCH_FIELD
    SERVICE_IMAGE = (By.XPATH, ".//ul[@class='services-new__list']//a[@data-id='images']")
    IMAGE_CATEGORY = (By.XPATH,
                      ".//div[contains(@class, 'PopularRequestList-Item')]//div[@class='PopularRequestList-Shadow']")
    IMAGE_IN_LIST = (By.XPATH, ".//div[@role='list']/div")
    IMAGE_WRAPPER = (By.CLASS_NAME, "MMImageWrapper")
    IMAGE = (By.XPATH, ".//img[@class='MMImage-Origin']")
    NEXT_IMAGE_BUTTON = (By.XPATH, ".//div[contains(@class, 'ButtonNext')]/i")
    PREV_IMAGE_BUTTON = (By.XPATH, ".//div[contains(@class, 'ButtonPrev')]/i")


class ImagesPage(BasePage):
    class ImageYandex:
        def __init__(self, src, byte):
            self.Src = src
            self.Byte = byte

    def __init__(self, driver):
        super().__init__(driver)
        self.PrevImage = self.ImageYandex(None, None)
        self.Image = self.ImageYandex(None, None)

    def check_image_link(self) -> WebElement:
        """
        Ищет ссылку "Картинки"

        :return: В случае успеха возвращает WebElement (Локатор: SERVICE_IMAGE)
        """
        return self.find_element(Locators.SERVICE_IMAGE)

    def open_image_page(self):
        """
        Ищет элемент (локатор SERVICE_IMAGE) и переходит по нему кликом. В случае, если ссылка открывается в новой
        вкладке, закрывает первую вкладку и переходит на последнюю открывшуюся.
        """
        self.find_and_click_element(Locators.SERVICE_IMAGE)
        if len(self.driver.window_handles) > 1:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

    def check_value_search_field(self) -> WebElement:
        """
        1. Ищет элемент (локатор IMAGE_CATEGORY) и переходит по нему кликом.
        2. Ищет элемент (локатор SEARCH_FIELD)

        :return: В случае успеха возвращает WebElement (Локатор: SEARCH_FIELD)
        """
        self.find_and_click_element(Locators.IMAGE_CATEGORY)
        search_value = self.find_element(Locators.SEARCH_FIELD)
        return search_value

    def check_open_image(self, time=10):
        """
        1. Ищет первый элемент (локатор IMAGE_IN_LIST) и переходит по нему кликом.
        2. Проверяет видимость картинки

        :param time: Время проверки, по умолчанию 10 сек;
        :return: В случае успеха возвращает WebElement (Локатор: IMAGE_WRAPPER)
        """
        self.find_and_click_element(Locators.IMAGE_IN_LIST)
        return WebDriverWait(self.driver, time)\
            .until(expected_conditions.visibility_of_element_located(Locators.IMAGE_WRAPPER))

    def get_class_image_yandex(self, arg):
        """
        Изменяет аргументы класса

        :param arg: Описаны в __init__
        """
        src = self.find_element(Locators.IMAGE).get_attribute('src')
        arg.Src, arg.Byte = src, Image.open(BytesIO(requests.get(src).content))

    def open_next_image(self):
        """
        Переходит к следующей картинке и изменяет аргументы
        """
        self.get_class_image_yandex(self.PrevImage)
        self.find_and_click_element(Locators.NEXT_IMAGE_BUTTON)
        self.get_class_image_yandex(self.Image)

    def open_prev_image(self):
        """
        Переходит к предыдущей картинке и изменяет аргументы
        """
        self.PrevImage.Src, self.PrevImage.Byte = self.Image.Src, self.Image.Byte
        self.find_and_click_element(Locators.PREV_IMAGE_BUTTON)
        self.get_class_image_yandex(self.Image)
