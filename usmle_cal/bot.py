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

    calendar_endpoint = "https://csess2.ecfmg.org/calendar.aspx?ssid=788446069625316DE053F603010A9402"

    calendar_request_headers = {
        "Cookie": None,
        "Host": "csess2.ecfmg.org",
        "Origin": "https://csess2.ecfmg.org",
        "Referrer": "https://csess2.ecfmg.org/calendar.aspx?ssid=788446069625316DE053F603010A9402"
    }
    
    def check_calendar(self):
        
        with requests.Session() as auth_session:
            login_response = auth_session.post(url=self.login_endpoint,
                                               json=self.login_request,
                                               headers=self.login_headers)
            self.calendar_request_headers["Cookie"] = "ASP.NET_SessionId=4syd0crtypuztj2jfkiwqtue; cssrdr=https://apps.nbme.org/nlesweb; ASPSESSIONIDAGTRDDTA=HKAMOFCDFGNGCGCAOLAJECHC; ASPSESSIONIDAGQTBCTB=IPDBBCPDLLGEECGFINDONDBH; .ASPXFORMSAUTH=AD58D79E8702D80A834DFC06061B011562F442019F66A2D78262BE7CF41F3A3201E0194A374A79731810748BE01422D3E4B8E927528B2A74795AFA42AB03A2605B2F8DBF48839A5B3DC19DD77C50B718935BF3176B4906D682C4B5E481927F32F9B71E05F1B30CBD7FAC636BED050C807B293E524912294FAB49488997AB7D201FAB31BCA3E7F1576ACC8BA8C29F0215B0F7261DFD40EA970594E24EAB81E43E42295F59D19B78EABE12CD735A5F2573393C8775CD6A9966E7D7CF1C65257153F808C14D9F7949BE16EF681077BC3C59"
            import pdb; pdb.set_trace()
            cal_response = auth_session.get(url=self.calendar_endpoint,
                                            headers=self.calendar_request_headers)
            


    
if __name__ == "__main__":
    AuthHandler().check_calendar()
        
