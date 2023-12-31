import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

capabilities_for_installation = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    language='en',
    locale='US'
)

capabilities_for_run = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='cz.alza.eshop',
    appActivity='cz.alza.base.android.setup.ui.activity.MainActivity',
    language='en',
    locale='US'
)

appium_server_url = 'http://localhost:4723'

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, capabilities_for_installation)
        print(">>>preparing and installation alza apk...")
        self.driver.install_app(app_path='resources\Alza_10.12.2_Apkpure.apk')
        self.driver = webdriver.Remote(appium_server_url, capabilities_for_run)
        print(">>>alza apk is succesfull installed...")

    def tearDown(self) -> None:
        self.driver.remove_app('cz.alza.eshop')
        print(">>>alza apk is uninstalled...")
        if self.driver:
            self.driver.quit()

    def test_registration_wrong(self) -> None:
        email = 'blud.com'
        phone_num = '35'
        password = '1234'
        confirm_password = '4321'

        signin_btn = self.driver.find_element(by=AppiumBy.XPATH, value='//android.view.View[@resource-id="IntroLoginSignUpButton"]')
        signin_btn.click()

        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//android.view.View[@resource-id="RegisterButton"]')))
        
        email_field = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="RegisterField"]')
        phone_field = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.EditText[@resource-id="RegisterPhoneField"]')
        password_field = self.driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.EditText[@resource-id="RegisterPasswordField"])[1]')
        confirm_pass_field = self.driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.EditText[@resource-id="RegisterPasswordField"])[2]')

        email_field.send_keys(email)
        phone_field.send_keys(phone_num)
        password_field.send_keys(password)
        confirm_pass_field.send_keys(confirm_password)
        
        email_wrong = self.driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.TextView[@text="Wrong format"])[1]')
        phone_wrong = self.driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.TextView[@text="Wrong format"])[2]')
        password_wrong = self.driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.TextView[@text="Passwords do not match"])[1]')
        confirm_pass_wrong = self.driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.TextView[@text="Passwords do not match"])[2]')
        time.sleep(1)
        register_btn = self.driver.find_element(by=AppiumBy.XPATH, value='//android.view.View[@resource-id="RegisterButton"]')
        register_btn_attr = register_btn.get_attribute('enabled')

        assert email_wrong.text == 'Wrong format'
        assert phone_wrong.text == 'Wrong format'
        assert password_wrong.text == 'Passwords do not match'
        assert confirm_pass_wrong.text == 'Passwords do not match'
        assert register_btn_attr == 'false'

if __name__ == '__main__':
    unittest.main()