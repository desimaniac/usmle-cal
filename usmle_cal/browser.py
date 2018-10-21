import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

from selenium.common.exceptions import NoSuchElementException


class ScheduleLinkFinder(object):
    def __call__(self, driver):
        try:
            available_dates_links = self.driver.find_elements_by_link_text(
                "View Available Test Dates")
            if available_dates_links:
                return True
        except:
            return False


class ScheduleButtonFinder(object):
    def __call__(self, driver):
        exam_buttons = driver.find_elements_by_css_selector(
            "button.btn.btn-sm.btn-block.btn-primary")
        if exam_buttons:
            return True
        return False


class SkipButtonFinder(object):
    def __call__(self, driver):
        try:
            skip_button = driver.find_element_by_name('btnSkip').click()
            if skip_button:
                return True
        except:
            return False


class USMLEBrowser(object):
    def __enter__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.binary_location =\
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

        desired = DesiredCapabilities.CHROME
        desired['loggingPrefs'] = {'browser': 'ALL', 'performance': 'ALL'}

        self.driver = webdriver.Chrome(
            executable_path=os.path.abspath("bin/chromedriver"),
            chrome_options=chrome_options,
            desired_capabilities=desired)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()

    def login(self):
        if hasattr(self, "driver"):
            self.driver.get("https://apps.nbme.org/nlesweb/#/login")
            # self.driver.save_screenshot("login_page.png")
            username = self.driver.find_element_by_id("USMLEID")
            password = self.driver.find_element_by_id("password")
            username.send_keys(os.environ.get("USMLE_ID"))
            password.send_keys(os.environ.get("PASSWORD"))

            self.driver.find_element_by_id("loginBtn").click()
            time.sleep(1)
            exam_buttons = self.driver.find_elements_by_css_selector(
                "button.btn.btn-sm.btn-block.btn-primary")
            exam_buttons[1].click()  # click the second one to reschedule
            time.sleep(1)
            # skip the emergency contact info
            self.driver.find_element_by_name('btnSkip').click()
            time.sleep(1)
            available_dates_links = self.driver.find_elements_by_link_text(
                "View Available Test Dates")
            if available_dates_links:
                available_dates_links[0].click()
                self.find_available_dates()
            else:
                import pdb
                pdb.set_trace()

    def find_available_dates(self):
        month_options = ["10-2018", "11-2018", "12-2018"]
        for x in range(0, 5):
            for month_option in month_options:
                city_link = self.driver.find_element_by_id(
                    "rdFacilityList_{}".format(x)).click()
                calendar_options = Select(
                    self.driver.find_element_by_id("sSelectCal"))
                calendar_options.select_by_value(month_option)
                # slow. as. fuck.
                for day in range(0, 30):
                    try:
                        available_day = self.driver.find_element_by_link_text(
                            str(day))
                        if available_day:
                            self.driver.execute_script(
                                "$('#recaptcha-anchor').setAttribute('aria-checked','true');")
                    except NoSuchElementException:
                        continue


# TODO: timeouts
def get_available_dates():
    with USMLEBrowser() as browser:
        browser.login()


if __name__ == "__main__":
    get_available_dates()
