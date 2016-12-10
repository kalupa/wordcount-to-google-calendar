#!python3
# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import
from datetime import datetime
import argparse
import httplib2
import json
import os
import string
import httplib2

# google modules
from googleapiclient import discovery
from oauth2client import file as ofile
from oauth2client import client
from oauth2client import tools

# pythonista modules
import appex
from console import hud_alert

APPLICATION_NAME = 'Daily Word Count Logger'

SCOPES = 'https://www.googleapis.com/auth/calendar'
BASE_DIR = os.path.expanduser('~')
DATA_PATH = os.path.join(BASE_DIR, 'Documents/data')
CLIENT_SECRET_FILE = os.path.join(DATA_PATH, 'client_secret.json')
CREDENTIAL_PATH = os.path.join(DATA_PATH, 'credentials-calendar.json')
CALENDAR_CONFIG = os.path.join(DATA_PATH, 'calendar.json')

def get_credentials():
    store = ofile.Storage(CREDENTIAL_PATH)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + CREDENTIAL_PATH)
    return credentials

def get_completion_time():
    return datetime.now().strftime('%H:%M')

def count_words(text):    
    stripped_text = text.strip(string.punctuation)
    return len(stripped_text.split())

def get_date_from_text(text):
    return text.splitlines()[0].lstrip('0 #')

def get_calendarid():
    jsonfile = open(CALENDAR_CONFIG)
    calendar_id = json.load(jsonfile)['id']
    jsonfile.close()
    return calendar_id

def create_calendar_event_from_text(text):
    event_date = {"date": get_date_from_text(text)}
    return {
        "end": event_date,
        "start": event_date,
        "summary": '%i Words' % count_words(text),
        "description": 'Completed %s' % get_completion_time()
    }   

def create_events_api_object():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    return service.events()

def _test_event_response(event):
    import time
    print(event)
    time.sleep(3)
    return event

def event_response(event):
    events = create_events_api_object()
    query = events.insert(calendarId=get_calendarid(), body=event)
    return query.execute()

def insert_daily_word_count_event(text):
    word_count_event = create_calendar_event_from_text(text)

    if appex.is_running_extension():
        return event_response(word_count_event)
    else:
        return _test_event_response(word_count_event)

def _test_text():
    hud_alert('Running with test data ...\n', 'success', 1)
    today = date.today().strftime('%Y-%m-%d')
    return ('# %s \n Lorem ipsum dolor sit amet, '
            'consectetur adipisicing elit, sed do eiusmod, '
            'tempor incididunt ut labore et dolore magna, '
            'aliqua.' % today)

def show_share_warning():
    hud_alert('This script is intended to be run from the sharing extension', 'error')
    return

def real_text():
    hud_alert('Running ...', 'success', 1)
    return appex.get_text()

def main():
    if not appex.is_running_extension():
        return show_share_warning()
        #text = _test_text()
    else:
        text = real_text()

    if text:
        result = insert_daily_word_count_event(text)
        hud_alert('Posted %s' % result['summary'], result['start']['date'])
    else:
        hud_alert('No input text found', 'error')

if __name__ == '__main__':
    main()
