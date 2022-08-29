import os
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

from datetime import date, timedelta

from sqlmodel import Session, col, select

from database import create_db_and_tables, engine
from models import Event
from utils import get_teslaquake_data, convert_to_event
from config import SQLITE_FILENAME, START_DATE_ISO_STR

def create_events(starttime: date, endtime: date):
    
    res = get_teslaquake_data(starttime, endtime)

    logging.info(f"Inserting data from {starttime} to {endtime}...")

    with Session(engine) as session:
        for e in res['features']:
            event = convert_to_event(e)
            session.add(event)
        session.commit()

    logging.info(f"Inserting data from {starttime} to {endtime} done.")



def main():
    if os.path.exists(SQLITE_FILENAME):
        os.remove(SQLITE_FILENAME)

    create_db_and_tables()

    #create_events(date.fromisoformat("1000-01-01"), date.fromisoformat("1950-01-01"))

    starttime = date.fromisoformat(START_DATE_ISO_STR)
    endtime = starttime + timedelta(weeks=1)
    
    for i in range(4*13):
        create_events(starttime + timedelta(weeks=1*i), endtime + timedelta(weeks=1*i))


if __name__ == "__main__":
    
    main()

    with Session(engine) as session:
        statement = select(Event).where(col(Event.mag) >= 1)
        events = session.exec(statement)
        for event in events:
            print(event)

