from datetime import datetime
import os
import sys

LOG_F_NAME = os.path.join(sys.path[0], "log.txt")


class Log:
    def __init__(self):
        if os.path.exists(LOG_F_NAME):
            self.f = open(LOG_F_NAME, "a")
        else:
            self.f = open(LOG_F_NAME, "w")

    def add(self, msg):
        dt = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
        full_msg = f"{dt}\t {msg}\n"
        self.f.write(full_msg)
