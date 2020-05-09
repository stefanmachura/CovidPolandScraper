from collections import namedtuple
import configparser

from bs4 import BeautifulSoup
import requests


def scrape_latest_data():
    config = configparser.ConfigParser()
    config.read("config.ini")

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
                DailyStats = namedtuple("DailyStats", ["date", "cases", "healthy", "delta"])
                return DailyStats(date, cases, healthy, delta)

