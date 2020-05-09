import smtplib

# change to context manager


def send_email(from_addr, to_addr, content, debug=True):
    if debug:
        server = smtplib.SMTP("192.168.2.234", port=1025)
        server.set_debuglevel(1)
    server.sendmail(from_addr, to_addr, content)
    server.quit()
