# positcloud

Posit Cloud, https://posit.cloud, is a platform that provides a collaborative environment for data science and analytics. It allows users to create, share, and run R and Python projects without the need to install anything locally.

The assignment is divided into two parts. The first part involves developing a test strategy to manually test the user interface in 15 minutes. Two documents were created for this purpose: `TestPlan.pdf` and `TestCases.pdf`. `TestPlan.pdf` provides an overview of the overall strategy and acts as a blueprint for the entire testing process. `TestCases.pdf`, on the other hand, details the individual test scenarios and offers specific instructions to follow during the testing.

The second part involves writing an automated test that logs into https://posit.cloud, creates a new space, creates a new RStudio project within that space, and waits for the RStudio IDE to load. The test is a Selenium-based Python script using the pytest testing framework. The Page Object Model (POM) design pattern is used to enhance code maintainability, reusability, and readability. The test logic is separated from the details of interacting with web elements. The high-level test logic is implemented in `test_rstudio_project_create.py`. The page object classes in the script include `home_page.py`, `login_page.py`, and `new_space_page.py`. This separation of concerns helps keep the test scripts clean and focused on high-level logic, while the page objects handle low-level interactions with web elements. Additionally, pytest fixture in `conftest.py` is used to define test inputs once and share them across multiple test functions, making the code more scalable as more tests are added. The `constants.py` file contains constants used throughout the scripts.

## SETUP FOR THE AUTOMATED SCRIPT
* Install [Python](https://www.python.org/search/?q=install&page=1) if it’s not already installed. 
  * Verify the installation by opening a command prompt or terminal and running the command: `python –-version`. It should display the installed Python version.
  ```
  (base) dev@ers-MacBook-Air-2 positcloud % python --version                     
  Python 3.12.7
  ```
* Install pytest.
  * From a command prompt or terminal, run the following command to install pytest using pip: 
  ```
  pip install pytest
  ```
* Install Selenium.
  * From a command prompt or terminal, run the following command to install Selenium using pip: 
  ```
  pip install selenium
  ```
* Download [chromedriver](https://developer.chrome.com/docs/chromedriver/downloads) to test on the Chrome browser.
  * Extract the downloaded file.
  * Move the extracted `chromedriver` executable to a directory that is included in your system’s `PATH` variable.


## RUN THE SCRIPT
* Edit `constants.py` to add your email and password for login.
  * Values were omitted from the file on purpose to avoid having them in plain text.
* From the terminal, run:
```
pytest test_rstudio_project_create.py
```

Here is an example of a successful test run
```shell
(base) dev@ers-MacBook-Air-2 positcloud % pytest test_rstudio_project_create.py
============================================== test session starts ==============================================
platform darwin -- Python 3.12.7, pytest-7.4.4, pluggy-1.0.0
rootdir: /Users/dev/PycharmProjects/Posit/positcloud
plugins: anyio-4.2.0
collected 1 item                                                                                                

test_rstudio_project_create.py .                                                                          [100%]

============================================== 1 passed in 28.31s ===============================================
```
Below is an example of a failed test (I modified the script to search for a non-existing web element in the step that validates if the RStudio IDE loads)
```shell
(base) dev@ers-MacBook-Air-2 positcloud % pytest test_rstudio_project_create.py
============================================== test session starts ==============================================
platform darwin -- Python 3.12.7, pytest-7.4.4, pluggy-1.0.0
rootdir: /Users/dev/PycharmProjects/Posit/positcloud
plugins: anyio-4.2.0
collected 1 item                                                                                                

test_rstudio_project_create.py F                                                                          [100%]

=================================================== FAILURES ====================================================
_________________________________ test_create_new_space_and_new_rstudioproject __________________________________

self = <pages.new_space_page.NewSpacePage object at 0x101ccf080>

    def verify_rstudio_ide_loads(self):
        # wait for RStudio IDE to load
        try:
            wait(self.driver, 90).until(EC.frame_to_be_available_and_switch_to_it("contentIFrame"))
>           ide = self.driver.find_element(By.XPATH, "//*[@id='rsXYZtudio_container']")

pages/new_space_page.py:38: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
/opt/anaconda3/lib/python3.12/site-packages/selenium/webdriver/remote/webdriver.py:898: in find_element
    return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
/opt/anaconda3/lib/python3.12/site-packages/selenium/webdriver/remote/webdriver.py:429: in execute
    self.error_handler.check_response(response)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <selenium.webdriver.remote.errorhandler.ErrorHandler object at 0x102c59340>
response = {'status': 404, 'value': '{"value":{"error":"no such element","message":"no such element: Unable to locate element: {\...0001862682e4 _pthread_start + 136\\n15  libsystem_pthread.dylib             0x00000001862630fc thread_start + 8\\n"}}'}

    def check_response(self, response: Dict[str, Any]) -> None:
        """Checks that a JSON response from the WebDriver does not have an
        error.
    
        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.
    
        :Raises: If the response contains an error message.
        """
        status = response.get("status", None)
        if not status or status == ErrorCode.SUCCESS:
            return
        value = None
        message = response.get("message", "")
        screen: str = response.get("screen", "")
        stacktrace = None
        if isinstance(status, int):
            value_json = response.get("value", None)
            if value_json and isinstance(value_json, str):
                import json
    
                try:
                    value = json.loads(value_json)
                    if len(value) == 1:
                        value = value["value"]
                    status = value.get("error", None)
                    if not status:
                        status = value.get("status", ErrorCode.UNKNOWN_ERROR)
                        message = value.get("value") or value.get("message")
                        if not isinstance(message, str):
                            value = message
                            message = message.get("message")
                    else:
                        message = value.get("message", None)
                except ValueError:
                    pass
    
        exception_class: Type[WebDriverException]
        e = ErrorCode()
        error_codes = [item for item in dir(e) if not item.startswith("__")]
        for error_code in error_codes:
            error_info = getattr(ErrorCode, error_code)
            if isinstance(error_info, list) and status in error_info:
                exception_class = getattr(ExceptionMapping, error_code, WebDriverException)
                break
        else:
            exception_class = WebDriverException
    
        if not value:
            value = response["value"]
        if isinstance(value, str):
            raise exception_class(value)
        if message == "" and "message" in value:
            message = value["message"]
    
        screen = None  # type: ignore[assignment]
        if "screen" in value:
            screen = value["screen"]
    
        stacktrace = None
        st_value = value.get("stackTrace") or value.get("stacktrace")
        if st_value:
            if isinstance(st_value, str):
                stacktrace = st_value.split("\n")
            else:
                stacktrace = []
                try:
                    for frame in st_value:
                        line = frame.get("lineNumber", "")
                        file = frame.get("fileName", "<anonymous>")
                        if line:
                            file = f"{file}:{line}"
                        meth = frame.get("methodName", "<anonymous>")
                        if "className" in frame:
                            meth = f"{frame['className']}.{meth}"
                        msg = "    at %s (%s)"
                        msg = msg % (meth, file)
                        stacktrace.append(msg)
                except TypeError:
                    pass
        if exception_class == UnexpectedAlertPresentException:
            alert_text = None
            if "data" in value:
                alert_text = value["data"].get("text")
            elif "alert" in value:
                alert_text = value["alert"].get("text")
            raise exception_class(message, screen, stacktrace, alert_text)  # type: ignore[call-arg]  # mypy is not smart enough here
>       raise exception_class(message, screen, stacktrace)
E       selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//*[@id='rsXYZtudio_container']"}
E         (Session info: chrome=134.0.6998.45); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#no-such-element-exception
E       Stacktrace:
E       0   chromedriver                        0x00000001004fbb78 cxxbridge1$str$ptr + 2778912
E       1   chromedriver                        0x00000001004f41b0 cxxbridge1$str$ptr + 2747736
E       2   chromedriver                        0x0000000100049e24 cxxbridge1$string$len + 92932
E       3   chromedriver                        0x0000000100091158 cxxbridge1$string$len + 384568
E       4   chromedriver                        0x00000001000d2500 cxxbridge1$string$len + 651744
E       5   chromedriver                        0x00000001000852e4 cxxbridge1$string$len + 335812
E       6   chromedriver                        0x00000001004c1d04 cxxbridge1$str$ptr + 2541740
E       7   chromedriver                        0x00000001004c4fc8 cxxbridge1$str$ptr + 2554736
E       8   chromedriver                        0x00000001004a2a44 cxxbridge1$str$ptr + 2414060
E       9   chromedriver                        0x00000001004c5828 cxxbridge1$str$ptr + 2556880
E       10  chromedriver                        0x0000000100493998 cxxbridge1$str$ptr + 2352448
E       11  chromedriver                        0x00000001004e43a4 cxxbridge1$str$ptr + 2682700
E       12  chromedriver                        0x00000001004e452c cxxbridge1$str$ptr + 2683092
E       13  chromedriver                        0x00000001004f3e24 cxxbridge1$str$ptr + 2746828
E       14  libsystem_pthread.dylib             0x00000001862682e4 _pthread_start + 136
E       15  libsystem_pthread.dylib             0x00000001862630fc thread_start + 8

/opt/anaconda3/lib/python3.12/site-packages/selenium/webdriver/remote/errorhandler.py:232: NoSuchElementException

During handling of the above exception, another exception occurred:

chrome_browser = <selenium.webdriver.chrome.webdriver.WebDriver (session="369c7a2bac2eaa712e09e06d89b0fc12")>

    def test_create_new_space_and_new_rstudioproject(chrome_browser):
        # open page
        home_page = HomePage(chrome_browser)
        home_page.open_page(constants.URL)
        home_page.click_login()
    
        # enter credentials to login
        login_page = LoginPage(chrome_browser)
        login_page.enter_email(constants.EMAIL)
        login_page.click_continue_button()
        login_page.enter_password(constants.PASSWD)
        login_page.click_login_button()
    
        new_space_page = NewSpacePage(chrome_browser)
        # create new space
        new_space_page.click_new_space()
        new_space_page.enter_space_name(constants.NEW_SPACE_NAME)
        new_space_page.click_create_button()
        new_space_page.click_newly_created_space()
        new_space_page.click_create_new_project()
        # create new RStudio project
        new_space_page.click_new_rstudio_project()
        # validate IDE loads
>       assert new_space_page.verify_rstudio_ide_loads()

test_rstudio_project_create.py:30: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <pages.new_space_page.NewSpacePage object at 0x101ccf080>

    def verify_rstudio_ide_loads(self):
        # wait for RStudio IDE to load
        try:
            wait(self.driver, 90).until(EC.frame_to_be_available_and_switch_to_it("contentIFrame"))
            ide = self.driver.find_element(By.XPATH, "//*[@id='rsXYZtudio_container']")
            return ide.is_displayed()
        except NoSuchElementException:
>           assert False, "RStudio IDE failed to load"
E           AssertionError: RStudio IDE failed to load

pages/new_space_page.py:41: AssertionError
============================================ short test summary info ============================================
FAILED test_rstudio_project_create.py::test_create_new_space_and_new_rstudioproject - AssertionError: RStudio IDE failed to load
========================================= 1 failed in 96.46s (0:01:36) ==========================================
```

## FUTURE IMPROVEMENTS
In addition to expanding the test suite with more automated test cases, it would have been beneficial to deploy both the solution and test environment as code using tools like Docker, Kubernetes, or Pulumi. This would eliminate the need for manual environment setup and help avoid the common "but it works in my machine" issue. In the current version, login credentials (email and password) are stored as plain text in a module, which is insecure. To improve security, secrets management tools such as HashiCorp Vault, Google Cloud Secret Manager, or AWS Secrets Manager should be used to securely store sensitive information. Additionally, a teardown process should be implemented to remove the RStudio project and space, ensuring the environment is ready for the next test execution. Finally, integrating the automated tests into a CI/CD pipeline would ensure that tests are executed with every build and deployment.