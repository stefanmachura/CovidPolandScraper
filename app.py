from bs4 import BeautifulSoup
import requests

SHEET_ID = "1400401584"

google_sheets = requests.get("https://docs.google.com/spreadsheets/d/1ierEhD6gcq51HAm433knjnVwey4ZE5DCnu1bW7PRG3E/htmlview#")

sheet_data = google_sheets.text

print(sheet_data)