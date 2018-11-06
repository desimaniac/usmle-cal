import os
import sched
import time
import pdb

import atexit
from slackclient import SlackClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


s = sched.scheduler(time.time, time.sleep)

slack_client = SlackClient(os.environ.get("SLACK_TOKEN"),
                           client_id=os.environ.get("SLACK_CLIENT_ID"),
                           client_secret=os.environ.get("SLACK_CLIENT_SECRET"))


class AvailableDates(object):
    def __init__(self, month_str, dates=[]):
        self.month_str = month_str
        self.dates = dates if dates else list(range(1, 32))


class USMLEBrowser(object):
    def __enter__(self):
        chrome_options = Options()
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
    
    def notify(self, title, text):
        os.system("""
                  osascript -e 'display notification "{}" with title "{}"'
                  """.format(text, title))
    
    def login(self):
        if hasattr(self, "driver"):
            self.driver.get("https://apps.nbme.org/nlesweb/#/login")

            username = self.driver.find_element_by_id("USMLEID")
            password = self.driver.find_element_by_id("password")

            username.send_keys(os.environ.get("USMLE_ID"))
            password.send_keys(os.environ.get("PASSWORD"))

            self.driver.find_element_by_id("loginBtn").click()

    def get_rescheduling_page(self):
        # TODO: change to find link by 'Browse Available Test Dates'
        if hasattr(self, "driver"):
            time.sleep(5)
            exam_buttons = self.driver.find_elements_by_css_selector(
                "button.btn.btn-sm.btn-block.btn-primary")            
            exam_buttons[1].click()  # click the second one to reschedule
            time.sleep(5)
            # skip the emergency contact info
            self.driver.find_element_by_name('btnSkip').click()
            time.sleep(5)

            available_dates_links = self.driver.find_elements_by_link_text(
                "View Available Test Dates")

            if available_dates_links:
                available_dates_links[0].click()
                self.find_available_dates()
            else:                
                pdb.set_trace()

    def alert_slack(self):
        for i in range(0, 3):
            slack_client.api_call('chat.postMessage',
                                  channel="#atlantopedia", 
                                  text="available date !! availability alert !!")

    def find_available_dates(self):
        month_options = [AvailableDates("11-2018"), AvailableDates("12-2018", list(range(1, 10)))]

        for month_option in month_options:
            city_link = self.driver.find_element_by_id(
                "rdFacilityList_3").click()
            try:
                calendar_options = Select(
                    self.driver.find_element_by_id("sSelectCal"))
            except StaleElementReferenceException as e:
                self.notify("ERROR", "{}".format(e))
                pdb.set_trace()

            calendar_options.select_by_value(month_option.month_str)
            
            for day in month_option.dates:
                try:
                    available_day = self.driver.find_element_by_link_text(str(day))
                    if available_day:
                        self.alert_slack()
                        pdb.set_trace()
                        available_day.click()
                        self.driver.execute_script(
                            "$('#recaptcha-anchor').setAttribute('aria-checked','true');")
                        confirm_button = self.driver.find_element_by_id("btnConfirm")

                        self.notify("DATE AVAILABLE", "{}".format(available_day))

                        confirm_button.click()

                except NoSuchElementException as e:
                    # Keep trying on schedule
                    continue

        print("no dates found")


def get_available_dates(sc):
    try:
        with USMLEBrowser() as browser:
            print("doing stuff")
            browser.login()
            browser.get_rescheduling_page()

    except NoSuchElementException as e:
        print(e)

    except TypeError as e:
        # This is not how I would normally handle errors, but for the purposes of speed
        print(e)
        print("Missing Env Vars")

    except IndexError as e:
        print(e)
        print("trying again")

    print("closing browser")
    s.enter(60, 1, get_available_dates, (sc,))

if __name__ == "__main__":
    response = slack_client.api_call('chat.postMessage',
                                     channel="#atlantopedia",
                                     text="starting up")
    
    s.enter(1, 1, get_available_dates, (s,))
    s.run()
