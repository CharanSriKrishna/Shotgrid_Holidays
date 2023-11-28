import requests
import json
import yaml


class sg_holiday:
    """
    Class to get the work with SG holidays
    """
    def __init__(self, host, username, password):
        # Website name, userid and _password
        self._host = host
        self._username = username
        self._password = password

        # Path to the access token in restapi
        self.access_token_path = '/api/v1/auth/access_token'
        # path to get to the work day rules
        self.work_day_path = '/api/v1/schedule/work_day_rules'

        # variable to store tokens
        self._access_token = None
        self._refresh_token = None
        self.__get_access_token_user()

    def __get_access_token_user(self):
        """
        Function to get the access token for the first time
        """
        # Defining headers for the request
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        }

        # defining the data for the request
        data = {
            "grant_type": "password",
            "username": self._username,
            "password": self._password
        }

        result = requests.post(f'{self._host}{self.access_token_path}', data=data, headers=headers)
        # converting the response to json format
        result = result.json()
        # Setting up the access tokens
        self._access_token = result['access_token']
        self._refresh_token = result['refresh_token']

    def __refresh_access_token(self):
        """
        Function to refresh the access token values
        """
        # Defining headers for the request
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        }

        # defining the data for the request
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
        }
        result = requests.post(f'{self._host}{self.access_token_path}', data=data, headers=headers)
        # converting the response to json format
        result = result.json()
        # Setting up the access tokens
        self._access_token = result['access_token']
        self._refresh_token = result['refresh_token']

    def get_dates(self, start, end, type):
        """
        Function to get the workday details based on the input
        :params
        start:start date from when the details are required format-"YYYY-MM-DD"
        end:end date till when the details are required format-"YYYY-MM-DD"
        type: what type of details you want all dates,working dates,holidays
        """
        # Refreshing the access token
        self.__refresh_access_token()

        # Defining headers for the request
        headers = {
            'Accept': 'application/json',
            'Authorization': f"Bearer {self._access_token}"
        }

        # Defining params for the request
        params = {
            'start_date': start,
            'end_date': end
        }
        # getting the workday details
        work_date = requests.get(f'{self._host}{self.work_day_path}', params=params, headers=headers)
        # converting the response to json format
        work_date = work_date.json()
        # if all the dates are needed
        if type == 'dates':
            return work_date['data']
        # if only the workdays are required
        elif type == 'working_dates':
            return self.__get_work_dates(work_date['data'])
        # if only the holidays are required
        else:
            return self.__get_holiday_dates(work_date['data'])

    def __get_work_dates(self, work_date):
        """
        function to filter out only the working dates
        """
        result = []
        for date in work_date:
            if date['working']:
                result.append(date)

        return result

    def __get_holiday_dates(self, work_date):
        """
        function to filter out only the working dates
        """
        result = []
        for date in work_date:
            if not date['working']:
                result.append(date)

        return result

    def add_holidays(self, params):
        """
        Function to add holidays to the SG
        :params params:dictionary with necessary details
        """
        # Refreshing the access token
        self.__refresh_access_token()

        # Defining headers for the request
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f"Bearer {self._access_token}"
        }
        # Defining data for the request
        data = json.dumps(params)
        result = requests.put(f'{self._host}{self.work_day_path}', params=params, data=data, headers=headers)
        result = result.json()
        return result

if __name__ == '__main__':
    # Getting the details from the yaml file
    with open('secret_holiday.yaml', 'r') as secrets_file:
        secrets = yaml.safe_load(secrets_file)

    # Getting the details if present
    host = secrets.get('host')
    username = secrets.get('username')
    password = secrets.get('password')

    # Creating a object of the class
    demo = sg_holiday(host, username, password)

