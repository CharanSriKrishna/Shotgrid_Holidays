from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle


class google_calender:
    def __init__(self):
        # scope is used to mention the path to the api we are using
        self.scope = ['https://www.googleapis.com/auth/calendar.readonly']

        # this defines the holiday group currently iam using the india calendar
        self.public_holidays_calendar_id = 'en.indian#holiday@group.v.calendar.google.com'

        # path to the token fil saved in local system to access again
        self.token_path = 'token.pickle'

        # variable to store credentials
        self.credentials = None

        # Function to get the credentials
        self.authenticate_and_authorize()

    def authenticate_and_authorize(self):
        """
        Function to log in to google and access the Google calendar api by generating and reading token
        """
        # if already signed in connects again with the previous session
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.credentials = pickle.load(token)

        # if the credentials are expired or invalid or other problems
        # connects again with Google to generate new sessions
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials._refresh_token:
                self.credentials.refresh(Request())
            else:
                # update this 'path_to_downloaded_credentials_in_json' with the path to your credentials
                flow = InstalledAppFlow.from_client_secrets_file(
                    'path_to_downloaded_credentials_in_json.json',
                    self.scope)
                self.credentials = flow.run_local_server(port=0)

            # Store the credential details as a pickle file in the local
            with open(self.token_path, 'wb') as token:
                pickle.dump(self.credentials, token)

    def get_national_holidays(self, start_date, end_date):
        """
        Function to get the holidays from the Google calendar api between the mentioned dates
        """

        # Building a service of the mentioned api
        service = build('calendar', 'v3', credentials=self.credentials)
        # Getting the list of all events within the dates
        events_result = service.events().list(
            calendarId=self.public_holidays_calendar_id,
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        dates = self._convert_to_sg_format(events)
        return dates

    def _convert_to_sg_format(self, events):
        """
        Function to convert the dates and events returned into a Shotgrid compatible form
        """
        dates = []
        if events:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                # Change the value of recalculated field based on you requirements refer the
                # necessary fields and types in readme
                date = {"date": str(start),
                        "working": False,
                        "recalculate_field": 'due_date',
                        "description": event['summary']
                        }
                dates.append(date)
        return dates

if __name__ == '__main__':
    # Specify the start and end dates for the date range
    start_date = '2022-10-01T00:00:00Z'  # Replace with your start date
    end_date = '2023-12-31T23:59:59Z'  # Replace with your end date
    demo = google_calender()
    dates = demo.get_national_holidays(start_date, end_date)
    for date in dates:
        print(date)
