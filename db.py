import configparser
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from scraping import DailyStats

config = configparser.ConfigParser()
config.read("config.ini")
url = "sqlite:///" + config["DB"]["DB_FILENAME"]

Base = declarative_base()


class DailyStat(Base):
    __tablename__ = "daily_stat"
    id = Column(Integer, primary_key=True)
    date = Column(String)
    cases = Column(String)
    healthy = Column(String)
    delta = Column(String)


engine = sqlalchemy.create_engine(url, echo=config["DEBUG"].getboolean("DEBUG_MODE"))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_to_db(date, cases, healthy, delta):
    first = DailyStat(date=date, cases=cases, healthy=healthy, delta=delta)
    session.add(first)
    session.commit()


def get_last_stat():
    last = session.query(DailyStat).order_by(DailyStat.id.desc()).first()
    if last == None:
        return DailyStats("", "", "", "")
    return DailyStats(last.date, last.cases, last.healthy, last.delta)

