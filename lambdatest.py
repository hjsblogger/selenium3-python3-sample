import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import warnings

username = os.getenv("LT_USERNAME")  # Replace the username
access_key = os.getenv("LT_ACCESS_KEY")  # Replace the access key

################################## @hjsblogger - Start ###########################
# The following exception is generated when using the options class
# with Selenium 3.141.0 and Python 3.9
# raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.WebDriverException: Message: unsupported platfrom any
################################## @hjsblogger - End #############################

# options = ChromeOptions()
# options.browser_version = "latest"
# # options.platform_name = "Windows 10"
# options.platform_name = "win10"
# lt_options = {}
# lt_options["username"] = username
# lt_options["accessKey"] = access_key
# lt_options["video"] = True
# lt_options["resolution"] = "1920x1080"
# lt_options["network"] = True
# lt_options["build"] = "test_build"
# lt_options["project"] = "unit_testing"
# lt_options["smartUI.project"] = "test"
# lt_options["name"] = "basic_unit_selenium"
# lt_options["w3c"] = True
# lt_options["plugin"] = "python-python"
# options.set_capability("LT:Options", lt_options)

################################## @hjsblogger - Start #############################################
# Instead of Options class, use Capabilities from https://www.lambdatest.com/capabilities-generator/
# Opt for browser capabilities over Options class
# Here the JSON wire protocol will be used instead of the W3C protocol
################################## @hjsblogger - End ###############################################

browser_capabilities = {
	"browserName": "Chrome",
	"browserVersion": "latest",
	"LT:Options": {
		"username": username,
		"accessKey": access_key,
		"platformName": "Windows 10",
        "selenium_version": "3.141.59",
		"project": "[Project] Python 3.9 + Selenium 3 Example",
        "build": "[Build] Python 3.9 + Selenium 3 Example"
	}
}

######################## @hjsblogger - Start ###############################
# Get these harmless malloc warnings that can be suppressed for the tests
# return self._request(command_info[0], url, body=data)
# ResourceWarning: Enable tracemalloc to get the object allocation traceback
################################## @hjsblogger - End  ######################

def suppress_resource_warnings():
    warnings.filterwarnings("ignore", category=ResourceWarning)

class FirstSampleTest(unittest.TestCase):
    driver = None

    def setUp(self):
        suppress_resource_warnings()
        self.driver = webdriver.Remote(
            command_executor = "http://{}:{}@hub.lambdatest.com/wd/hub".format(
                username, access_key
            ),
            # options=options,
            desired_capabilities = browser_capabilities
        )

    # """ You can write the test cases here """
    def test_demo_site(self):
        suppress_resource_warnings()
        driver = self.driver
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        driver.set_window_size(1920, 1080)

        # Url
        print("Loading URL")
        driver.get(
            "https://lambdatest.github.io/sample-todo-app/"
        )

        # Let's click on a element
        driver.find_element(By.NAME, "li1").click()
        location = driver.find_element(By.NAME, "li2")
        location.click()
        print("Clicked on the second element")

        # Let's add a checkbox
        driver.find_element(By.ID, "sampletodotext").send_keys("LambdaTest")
        add_button = driver.find_element(By.ID, "addbutton")
        add_button.click()
        print("Added LambdaTest checkbox")

        # print the heading
        search = driver.find_element(By.CSS_SELECTOR, ".container h2")
        assert search.is_displayed(), "heading is not displayed"
        print(search.text)
        search.click()
        driver.implicitly_wait(3)

        # Let's download the invoice
        heading = driver.find_element(By.CSS_SELECTOR, ".container h2")
        ################### @hjsblogger - Start ##########################
        # Handled in the tearDown, can't add the pass/logic for every step
        # if heading.is_displayed():
        #     heading.click()
        #     driver.execute_script("lambda-status=passed")
        #     print("Tests are run successfully!")
        # else:
        #     driver.execute_script("lambda-status=failed")
        ################### @hjsblogger - End ############################

    # tearDown runs after each test case
    def tearDown(self):
        # Mark the test status in LambdaTest based on whether it passed or failed
        if hasattr(self, '_outcome'):
            if self._outcome.errors[1][1] is None:
                self.driver.execute_script("lambda-status=passed")
            else:
                self.driver.execute_script("lambda-status=failed")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()