import constant
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.new_space_page import NewSpacePage

# Verify that the user can create a new space and create an RStudio Project within that space
def test_create_new_space_and_new_rstudioproject(chrome_browser):
    # open page
    home_page = HomePage(chrome_browser)
    home_page.open_page(constant.URL)
    home_page.click_login()

    # enter credentials to login
    login_page = LoginPage(chrome_browser)
    login_page.enter_email(constant.EMAIL)
    login_page.click_continue_button()
    login_page.enter_password(constant.PASSWD)
    login_page.click_login_button()

    new_space_page = NewSpacePage(chrome_browser)
    # create new space
    new_space_page.click_new_space()
    new_space_page.enter_space_name(constant.NEW_SPACE_NAME)
    new_space_page.click_create_button()
    new_space_page.click_newly_created_space()
    new_space_page.click_create_new_project()
    # create new RStudio project
    new_space_page.click_new_rstudio_project()
    # validate IDE loads
    assert new_space_page.verify_rstudio_ide_loads()