from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import Keys.cal_id as cal_id
import datetime
from datetime import date, time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'Keys/client_secret.json'
APPLICATION_NAME = 'Fridge Magnet'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'googleCalCreds.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.now().isoformat() + 'Z' 

    today_beginning = datetime.datetime.combine(date.today(), time())
    today_end = today_beginning + datetime.timedelta(2, 0)# - datetime.timedelta(0, 1)

    today_beginning = today_beginning.isoformat() + 'Z'
    today_end = today_end.isoformat() + 'Z'

    print(today_end, today_beginning)

    # Initiate event request
    eventsResult = service.events().list(
        calendarId=cal_id.calendarId, timeMin=today_beginning, timeMax=today_end).execute()

    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    else:
        print('Events scheduled for today:')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

if __name__ == '__main__':
    main()