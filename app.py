import db
import mail
import scraping

newest_scraped = scraping.scrape_latest_data()

newest_from_db = db.get_last_stat()

print(newest_scraped)
print(newest_from_db)

if not newest_scraped == newest_from_db:
    content = f"""\
    Subject: New COVID data received!

    Date: {newest_scraped.date}
    Healthy: {newest_scraped.healthy}
    Delta: {newest_scraped.delta}
    Cases:{newest_scraped.cases}
    """
    mail.send_email(from_addr="", to_addr="", content=content, debug=False)
    db.add_to_db(newest_scraped.date, newest_scraped.cases, newest_scraped.healthy, newest_scraped.delta)
else:
    print("no changes!")
