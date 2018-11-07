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

The below cd could be avoided by adding the location of the chromedriver install to your PATH, but for ease:

```bash
cd usmle_cal 
python browser.py
```
