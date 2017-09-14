__author__ = "Kris"
import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta
# from project.google_apis.sheets_api import GOOGLE_SHEETS_DUMMY_LIST


#####################################
# Run settings
#####################################
LOCAL_RUN = False
DISTANCE_MATRIX = "api" # 'api' or 'dummy'
GOOGLE_SPREADSHEET = "dummy" # 'api' or 'dummy'

#####################################
# Google Sheets API settings
#####################################
SHEETS_API_CREDENTIALS = "client_secret.json"
WORKBOOK = "19oxjhPkCo5tW5D_emRr5cO4GCCsAgvESc5VCGXeJ8L8"
SHEET = "Sheet1"


#####################################
# Google Distance Matrix API Settings
#####################################
TRAFFIC_MODEL = 'pessimistic'  # Options are 'pessimistic', 'optimistic', and 'best_guess
MODE = 'driving'  # options are 'driving', 'walking', 'cycling', 'transit'
DEPARTURE_WEEKDAY = 2  # 0: Monday, 1: Tuesday, 2: Wednesday, etc
weekday = datetime.today().weekday()
DEPARTURE_TIME = datetime.utcnow() + relativedelta(weekday=DEPARTURE_WEEKDAY if weekday != 2 else 3,
                                                   hour=14, minute=0, second=0)
GEOCODE_BASE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"

#####################################
# General Settings
#####################################
pp = pprint.PrettyPrinter()
CMDC_API = ""