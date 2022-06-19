import allure
import pytest
from PIL import ImageChops

from pages.images import ImagesPage
from tests.report import allure_screenshot

driver: ImagesPage

@allure.feature('Yandex image')
@allure.story('1. Проверяем наличие ссылка "Картинки"')
def test_image_link(start_driver):
    global driver
    driver = ImagesPage(start_driver)
    driver.get()
    allure_screenshot(driver, 'test_image_link')
    assert driver.check_image_link()

@allure.feature('Yandex image')
@allure.story('2. Проверяем ссылку')
def test_url_image_page():
    driver.open_image_page()
    assert driver.driver.current_url == 'https://yandex.ru/images/'

@allure.feature('Yandex image')
@allure.story('3. Проверяем заполнено ли поле поиска')
def test_check_value_search_field():
    search_value = driver.check_value_search_field()
    allure_screenshot(driver, 'test_check_value_search_field')
    assert search_value.get_attribute('value') != ''

@allure.feature('Yandex image')
@allure.story('4. Проверка открытия картинки')
def test_open_image():
    element = driver.check_open_image()
    allure_screenshot(driver, 'test_open_image')
    assert element

@allure.feature('Yandex image')
@allure.story('5. Проверяем изменилась ли картинка')
class TestOpenNextImage:
    def test_src(self):
        """
        Сравнивает url картинок
        """
        driver.open_next_image()
        allure_screenshot(driver, 'TestOpenNextImage')
        assert driver.PrevImage.Src != driver.Image.Src

    def test_pixels(self):
        """
        Сравнивает пиксели
        """
        assert ImageChops.difference(driver.PrevImage.Byte, driver.Image.Byte).getbbox() is not None

@allure.feature('Yandex image')
@allure.story('6. Проверяем изменилась ли картинка на прежнюю')
class TestOpenPrevImage:
    @pytest.fixture
    def prev_image(self):
        return {'src': driver.PrevImage.Src, 'bytes': driver.PrevImage.Byte}

    def test_src(self, prev_image):
        """
        Сравнивает url картинок
        """
        driver.open_prev_image()
        allure_screenshot(driver, 'TestOpenPrevImage')
        assert driver.PrevImage.Src != prev_image['src']

    def test_pixels(self, prev_image):
        """
        Сравнивает пиксели
        """
        assert ImageChops.difference(prev_image['bytes'], driver.Image.Byte).getbbox() is not None
