from google_calender_holiday_api import google_calender as gc
from sg_holidy_api import sg_holiday as sgh
import yaml

# opening the yaml file and reading the necessary details
with open('secret_holiday.yaml', 'r') as secrets_file:
    secrets = yaml.safe_load(secrets_file)

# Getting the host, username, password
host = secrets.get('host')
username = secrets.get('username')
password = secrets.get('password')

# getting the dates
start_date = secrets.get('start_date')
end_date = secrets.get('end_date')

# create the google calendar class
google_calendar = gc()
dates = google_calendar.get_national_holidays(start_date, end_date)

# Create the Shotgrid calendar class
shotgrid_holiday = sgh(host, username, password)
print(dates)
# adding each dates in shotgrid
for date in dates:
    print(shotgrid_holiday.add_holidays(date))

