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
import time as sleeper
import Hardware.PI2LCD as lcd
import weather_man

kelvin_to_celcius = 272.15
sleep_time = 50
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

def pollingFunction():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    today_beginning = datetime.datetime.combine(date.today(), time())
    today_end = today_beginning + datetime.timedelta(2, 0) - datetime.timedelta(0,1)

    today_beginning = today_beginning.isoformat() + 'Z'
    today_end = today_end.isoformat() + 'Z'

    # Initiate event request
    eventsResult = service.events().list(
        calendarId=cal_id.calendarId, singleEvents='True', timeMax=today_end).execute()

    return (eventsResult.get('items', []), today_beginning)

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def parseEvents(events, today_beginning):
    today_counter = 0
    summary_list = []
    for event in events:
        dateStr = 'dateTime' if 'dateTime' in event['start'] else 'date'
        if event['start'][dateStr][:10] == today_beginning[:10]:
            start = event['start'].get('dateTime', event['start'].get('date'))
            today_counter = today_counter + 1
            summary_list.append((start,event['summary']))
    if today_counter == 0:
        print('No events found for today.')
    else:
	#Remove last newline
        return summary_list

def disp_loop(arr):
	for item in arr:
		lcd.write_to_LCD(item[0][11:19], item[1])
		sleeper.sleep(5)

def main():
    while True:
        lcd.clear_LCD()
        outTup = pollingFunction()
        retArr = parseEvents(outTup[0], outTup[1])
        disp_loop(retArr)
        sleeper.sleep(sleep_time)
        lcd.clear_LCD()
        outWeather = weather_report()
        lcd.write_to_LCD(outWeather['status'], outWeather['temp'])
        sleeper.sleep(sleep_time)
	
def weather_report():
    ret_obj = {}
    weather_raw = weather_man.main()
    temp_report = weather_raw['main']
    descrip = weather_raw['weather'][0]
    ret_obj['temp'] = round(temp_report['temp'] - kelvin_to_celcius)
    ret_obj['status'] = descrip['description']
    return ret_obj
    


if __name__ == "__main__":
    main()
