from collections import namedtuple
import configparser
import os
import sys

from bs4 import BeautifulSoup
import requests

DailyStats = namedtuple("DailyStats", ["date", "cases", "healthy", "delta"])


def scrape_latest_data():
    """
    read latest data from "Covic-19 w Polsce" Google Sheet
    returns a namedtuple with the most current statistics
    """
    config = configparser.ConfigParser()
    config.read(os.path.join(sys.path[0], "config.ini"))

    google_sheets = requests.get(config["GSHEETDATA"]["GSHEET_URL"])
    covid_data = BeautifulSoup(google_sheets.text, "html.parser")
    stats = covid_data.find(id=config["GSHEETDATA"]["SHEET_ID"])

    rows = stats.find_all("tr")
    for row in rows[::-1]:
        cells = row.find_all("td")
        if len(cells) > 0:
            date = cells[0].text
            cases = cells[int(config["GSHEETDATA"]["CASES_SUM_COLUMN"])].text
            healthy = cells[int(config["GSHEETDATA"]["RECOVERED_COLUMN"])].text
            delta = cells[int(config["GSHEETDATA"]["DELTA_COLUMN"])].text
            if cases.isdigit() or healthy.isdigit() or delta.isdigit():
                return DailyStats(date, cases, healthy, delta)
