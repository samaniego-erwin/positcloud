from selenium.webdriver.common.by import By

class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def open_page(self, url):
        self.driver.get(url)

    def click_login(self):
        self.driver.find_element(By.XPATH ,"//span[normalize-space()='Log In']").click()