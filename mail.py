import configparser
import smtplib

config = configparser.ConfigParser()
config.read("config.ini")
SMTP_CONFIG = config["SMTP"]

# change to context manager


def send_email(from_addr, to_addr, content, debug=True):
    if debug:
        try:
            server = smtplib.SMTP(SMTP_CONFIG["DEBUG_SERVER"], SMTP_CONFIG["DEBUG_PORT"])
            server.set_debuglevel(1)
            server.sendmail(from_addr, to_addr, content)
        except:
            print('Something went wrong...')
        finally:
            server.close()
    else:
        try:
            server = smtplib.SMTP_SSL(SMTP_CONFIG["SERVER"], SMTP_CONFIG["PORT"])
            server.ehlo()
            server.login("x", "x")
            server.sendmail(from_addr, to_addr, content)
        except Exception as e:
            print(f'Something went wrong... {e}')
        finally:
            server.close()
    
    
