import allure
from allure_commons.types import AttachmentType

def allure_screenshot(driver, name: str):
    with allure.step('Скриншот'):
        allure.attach(driver.get_screenshot_as_png(),
                      name=f'screenshot_{name}',
                      attachment_type=AttachmentType.PNG)