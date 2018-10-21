import json
import os

import requests

class AuthHandler(object):
    login_endpoint = "https://apps.nbme.org/nlesservice/webaccess/loginUser"

    login_request = {
        "usmleId": os.environ.get("USMLE_ID"),
        "password": os.environ.get("PASSWORD"),
        "snId": None
    }

    login_headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Auth-Credentials": "public,nlesuser",
        "Auth-Principale": "lesusern",
        "Host": "apps.nbme.org",
        "Origin": "https://apps.nbme.org",
        "Referrer": "https://apps.nbme.org/nlesweb",
        "X-Auth-Token": "initialized",
    }

    calendar_endpoint = "https://csess2.ecfmg.org/calendar.aspx?ssid={}".format(os.environ.get("SSID"))

    calendar_request_headers = {
        "Cookie": None,
        "Host": "csess2.ecfmg.org",
        "Origin": "https://csess2.ecfmg.org",
        "Referrer": "https://csess2.ecfmg.org/calendar.aspx?ssid={}".format(os.environ.get("SSID"))
    }
    
    def check_calendar(self):
        
        with requests.Session() as auth_session:
            login_response = auth_session.post(url=self.login_endpoint,
                                               json=self.login_request,
                                               headers=self.login_headers)
            # run through login response cookies and retrieve
            if os.environ.get("BROWSER_COOKIE"):
                self.calendar_request_headers["Cookie"] = os.environ.get("BROWSER_COOKIE")
            import pdb; pdb.set_trace()
            cal_response = auth_session.get(url=self.calendar_endpoint,
                                            headers=self.calendar_request_headers)

    
if __name__ == "__main__":
    AuthHandler().check_calendar()
