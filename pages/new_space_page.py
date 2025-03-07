from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

# NewSpacePage class for posit.cloud
class NewSpacePage:
    def __init__(self, driver):
        self.driver = driver

    def click_new_space(self):
        # New space element
        self.driver.find_element(By.XPATH, "//span[normalize-space()='New Space']").click()

    def enter_space_name(self, name):
        self.driver.find_element(By.XPATH, "//input[@id='name']").send_keys(name)

    def click_create_button(self):
        self.driver.find_element(By.XPATH, "//span[normalize-space()='Create']").click()

    def click_newly_created_space(self):
        # Element for the user created space
        self.driver.find_element(By.XPATH, "//div[@class='spaceNameWithOwner']").click()

    def click_create_new_project(self):
        self.driver.find_element(By.XPATH, "//span[normalize-space()='New Project']").click()

    def click_new_rstudio_project(self):
        self.driver.find_element(By.XPATH, "//span[normalize-space()='New RStudio Project']").click()

    def find_rstudio_ide(self):
        self.driver.find_element(By.XPATH, "//iframe[@id='contentIFrame']")

    def verify_rstudio_ide_loads(self):
        # wait for RStudio IDE to load
        try:
            wait(self.driver, 90).until(EC.frame_to_be_available_and_switch_to_it("contentIFrame"))
            ide = self.driver.find_element(By.XPATH, "//*[@id='rstudio_container']")
            return ide.is_displayed()
        except NoSuchElementException:
            assert False, "RStudio IDE failed to load"


