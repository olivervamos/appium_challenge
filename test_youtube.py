import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='com.google.android.youtube',
    appActivity='com.google.android.apps.youtube.app.watchwhile.WatchWhileActivity',
    language='en',
    locale='US'
)

appium_server_url = 'http://localhost:4723'

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, capabilities)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_search(self) -> None:
        text_to_find = 'Hamilton Pilot Pioneer'
        
        allow_btn = self.driver.find_element(by=AppiumBy.ID, value='com.android.permissioncontroller:id/permission_allow_button')
        allow_btn.click()
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//android.widget.ImageView[@content-desc="Search"]')))

        search_btn = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageView[@content-desc="Search"]')
        search_btn.click()
        
        search_field = self.driver.find_element(by=AppiumBy.CLASS_NAME, value='android.widget.EditText')
        search_field.send_keys(text_to_find)
        self.driver.keyevent(keycode=66)
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//android.support.v7.widget.RecyclerView[@resource-id="com.google.android.youtube:id/results"]/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup')))
        
        self.driver.swipe(200, 200, 0, 1000)
        videos_btn = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="com.google.android.youtube:id/text" and @text="Videos"]')
        videos_btn.click()
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//android.view.ViewGroup[contains(@content-desc,"Hamilton - Khaki Aviation")]')))
         
        result = self.driver.find_element(by=AppiumBy.XPATH, 
                                               value='//android.view.ViewGroup[contains(@content-desc,"Hamilton - Khaki Aviation")]')

        result_text = result.get_attribute('content-desc')
        list_for_assert = list(text_to_find.split(" "))
        list_from_result = list(result_text.split(" "))

        for i in range(len(list_for_assert)):
             match = list_for_assert[i]
             assert match in list_from_result
    

if __name__ == '__main__':
    unittest.main()