# USMLE Cal

A super quick spin up as a favor to automate a calendar sign up process with Selenium that was too cumbersome with scraper tools like BeautifulSoup.


## Setup

Requisite config values can be found in env.dist. Suggested:

```bash
cp env.dist env.<YOUR_ENV>.sh
```

Source these into the environment

```bash
source env.<YOUR_ENV>.sh
```

To get chromedriver for selenium, run:

```bash
./setup.sh
```

Set up a virtual environment of your choice and run
```bash
pip install -r requirements.txt
```

## To Run

```bash
python usmle_cal/browser.py
```
