import configparser
from email.message import EmailMessage
import os
import smtplib
import sys

import log

config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], "config.ini"))
SMTP_CONFIG = config["SMTP"]

log = log.Log()


def send_email(to_addr, subject, content, debug=True):
    if not all([x in os.environ for x in ["SMTP_LOGIN", "SMTP_PASS", "SMTP_FROM"]]):
        log.add("env variables missing")
        raise KeyError("missing environmental variables needed for SMTP!")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.environ.get("SMTP_FROM")
    msg["To"] = to_addr
    msg.set_content(content)

    try:
        if debug:
            server = smtplib.SMTP(
                SMTP_CONFIG["DEBUG_SERVER"], SMTP_CONFIG["DEBUG_PORT"]
            )
            server.set_debuglevel(1)
            server.send_message(msg)
        else:
            server = smtplib.SMTP_SSL(SMTP_CONFIG["SERVER"], SMTP_CONFIG["PORT"])
            server.ehlo()
            server.login(os.environ.get("SMTP_LOGIN"), os.environ.get("SMTP_PASS"))
            server.send_message(msg)
    except Exception as e:
        log.add(e)
    finally:
        server.close()
