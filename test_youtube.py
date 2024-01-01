import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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
        text_to_find = 'Teddy Baldassarre'
        
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'com.android.permissioncontroller:id/permission_allow_button')))
            allow_btn = self.driver.find_element(by=AppiumBy.ID, value='com.android.permissioncontroller:id/permission_allow_button')
            allow_btn.click()
        except:
            pass
        
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
        try:
            videos_btn = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="com.google.android.youtube:id/text" and @text="Videos"]')
            videos_btn.click()
        except:
            pass

        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, f'//android.view.ViewGroup[contains(@content-desc,"{text_to_find}")]')))
        result = self.driver.find_element(by=AppiumBy.XPATH, 
                                               value=f'//android.view.ViewGroup[contains(@content-desc,"{text_to_find}")]')

        result_text = result.get_attribute('content-desc')
        result_text = result_text.replace(".", "")
        expected_list = list(text_to_find.split(" "))
        print(f'text to find: {expected_list}')
        list_from_result = list(result_text.split(" "))
        print(f'list with values for assert: {list_from_result}')

        for i in range(len(expected_list)):
             match = expected_list[i]
             assert match in list_from_result

if __name__ == '__main__':
    unittest.main()