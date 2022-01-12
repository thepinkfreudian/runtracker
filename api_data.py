import os
import pandas as pd
from datetime import datetime
from setup import config, start_date, end_date

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

secrets = config['secrets']
token_file = config['token_file']

scopes = ['https://www.googleapis.com/auth/fitness.location.read']
datasource = 'derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta'
dataset = ''  # set after function defs


def date_to_ns(date):
    dt = datetime.strptime(date + ' 00:00:00,76', '%m/%d/%Y %H:%M:%S,%f')
    nano_dt = dt.timestamp() * 1000000000

    return int(nano_dt)


def ns_to_date(ns):
    dt = datetime.fromtimestamp(ns // 1000000000)

    return dt.strftime('%Y-%m-%d')


def get_credentials(token_file, secrets, scopes):
    credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        credentials = Credentials.from_authorized_user_file(token_file, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                secrets, scopes)
            credentials = flow.run_local_server(port = 0)
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(credentials.to_json())

    return credentials


def get_api_data(dataset, datasource):
    try:
        service = build('fitness', 'v1', credentials=credentials)
        response = service.users().dataSources().datasets().get(userId='me',
                                                                dataSourceId=datasource,
                                                                datasetId=dataset).execute()

    except HttpError as err:
        print(err)

    return response


start_date_ns = date_to_ns(start_date)
end_date_ns = date_to_ns(end_date)
dataset = str(start_date_ns) + '-' + str(end_date_ns)

credentials = get_credentials(token_file, secrets, scopes)
response = get_api_data(dataset, datasource)

points = response['point']
data = pd.DataFrame(columns=['start_date', 'end_date', 'miles'])

for i in range(0, len(points)):
    start_date = ns_to_date(int(points[i]['startTimeNanos']))
    end_date = ns_to_date(int(points[i]['endTimeNanos']))
    miles = int(points[i]['value'][0]['fpVal']) * 0.000621371  # m to mi
    row = [start_date, end_date, miles]
    data.loc[len(data)] = row

api_data = data.groupby('start_date', as_index=False)['miles'].sum()
