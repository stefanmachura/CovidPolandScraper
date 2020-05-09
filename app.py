import configparser
import db
import log
import mail
import scraping

config = configparser.ConfigParser()
config.read("config.ini")

with open("recipients.txt", "r") as recip_file:
    recipients = recip_file.readlines()

log = log.Log()

newest_scraped = scraping.scrape_latest_data()
newest_from_db = db.get_last_stat()


if newest_scraped != newest_from_db:
    content = f"""\
    Here are the newest statistics:
    Date: {newest_scraped.date}
    Healthy: {newest_scraped.healthy}
    Delta: {newest_scraped.delta}
    Cases: {newest_scraped.cases}
    """
    for recipient in recipients:
        mail.send_email(
            to_addr=recipient,
            subject="New COVID data received!",
            content=content,
            debug=config["DEBUG"].getboolean("DEBUG_MODE"),
        )
    db.add_to_db(
        newest_scraped.date,
        newest_scraped.cases,
        newest_scraped.healthy,
        newest_scraped.delta,
    )
    log.add("Changes found, emails sent")
else:
    log.add("Checked, no changes found")
