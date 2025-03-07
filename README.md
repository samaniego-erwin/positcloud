# positcloud

The assignment was to write an automated test that logs into https://posit.cloud, creates a new space, creates a new RStudio project within that space, and waits for the RStudio IDE to load. The script is a Selenium-based Python script using the pytest testing framework. The Page Object Model (POM) design pattern is used to enhance code maintainability, reusability, and readability. The test logic is separated from the details of interacting with web elements. The high-level test logic is implemented in `test_rstudio_project_create.py`. The page object classes in the script include `home_page.py`, `login_page.py`, and `new_space_page.py`. This separation of concerns helps keep the test scripts clean and focused on high-level logic, while the page objects handle low-level interactions with web elements. Additionally, pytest fixture in `conftest.py` is used to define test inputs once and share them across multiple test functions, making the code more scalable as more tests are added. The `constants.py` file contains constants used throughout the scripts.

## SETUP
* Install [Python](https://www.python.org/search/?q=install&page=1) if it’s not already installed. 
  * Verify the installation by opening a command prompt or terminal and running the command: `python –-version`. It should display the installed Python version.
  ```
  (base) dev@ers-MacBook-Air-2 positcloud % python --version                     
  Python 3.12.7
  ```
* Install pytest.
  * From a command prompt or terminal and run the following command to install pytest using pip: 
  ```
  pip install pytest
  ```
* Install Selenium.
  * From a command prompt or terminal and run the following command to install Selenium using pip: 
  ```
  pip install selenium
  ```
* Download [chromedriver](https://developer.chrome.com/docs/chromedriver/downloads) to test on the Chrome browser.
  * Extract the downloaded file.
  * Move the extracted `chromedriver` executable to a directory that is included in your system’s `PATH` variable.


## RUN THE SCRIPT
*Edit `constants.py` to add your email and password for login.
  * Values were omitted from the file on purpose to avoid having them in plain text.
*From the terminal, run:
```
pytest test_rstudio_project_create.py
```

## FUTURE IMPROVEMENTS
In addition to expanding the test suite with more automated test cases, it would have been beneficial to deploy the solution and test environment as code using tools like Docker, Kubernetes, Pulumi. This approach would eliminate the need for manual environment setup and resolve the common issue of "but it works in my environment." In this version, the login credentials (email and password) are stored in a module as plain text, which is insecure. To address this, secrets management tools such as HashiCorp Vault, Google Cloud Secret Manager, or AWS Secrets Manager should be used to store sensitive data securely. Furthermore, the automated tests should be integrated into a CI/CD pipeline to ensure that tests are run with every build and deployment.