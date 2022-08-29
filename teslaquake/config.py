import os

DEBUG = False
#START_DATE_ISO_STR = "1950-01-01"
START_DATE_ISO_STR = "2017-01-01"
TESLAQUAKE_COLUMNS = ['id', 'type', 'place', 'time', 'latitude', 'longitude', 'depth', 'magType', 'mag']
TESLAQUAKE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
TESLAQUAKE_EVENTS = [
    'other event', 
    'industrial explosion', 
    'volcanic eruption', 
    'chemical explosion', 
    'sonic boom', 
    'mine collapse', 
    'quarry blast', 
    'explosion', 
    'nuclear explosion', 
    'rock burst', 
    'earthquake'
]


SQLITE_FILENAME = "database.db"

#TESLAQUAKE_DATABASE_URL = f"sqlite:///{SQLITE_FILENAME}"
TESLAQUAKE_DATABASE_URL = os.environ['TESLAQUAKE_DATABASE_URL']