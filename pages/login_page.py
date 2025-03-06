from selenium.webdriver.common.by import By

# LoginPage class for posit.cloud
class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_email(self, email):
        self.driver.find_element(By.NAME, "email").send_keys(email)

    def click_continue_button(self):
        # Continue button element
        self.driver.find_element(By.XPATH, "//body/div[@id='app']/div[@id='main']/div[@class='band pushFooter']/div[@id='entry']/div[@class='fullPageFormContainer marginAbove']/form/fieldset[@class='actions noMarginAbove']/button[1]").click()

    def enter_password(self, passwd):
        self.driver.find_element(By.NAME, "password").send_keys(passwd)

    def click_login_button(self):
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
