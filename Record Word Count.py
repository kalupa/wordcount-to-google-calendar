#!python3
# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import
import argparse
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

TEST_FILE = os.path.join(DATA_PATH, 'test-file.md')

def main():
    if not appex.is_running_extension():
        return show_share_warning()
        # text = test_text()
    else:
        text = real_text()

    if text:
        result = insert_daily_word_count_event(text)
        hud_alert('Posted %s' % result['summary'], 
                    result['start']['date'])
    else:
        hud_alert('No input text found', 'error')
        
def show_share_warning():
    return hud_alert('This script is intended '
                      'to be run from the '
                      'sharing extension', 'error')

def real_text():
    hud_alert('Running ...', 'success', 1)
    
    # Some apps share the file path of the text (Ulysses) 
    # while others will send the text content (iA Writer)
    file_path = appex.get_file_path()
    if file_path is not None:
        return _read_file(file_path)
    else:
        return appex.get_text()
        
def insert_daily_word_count_event(text):
    word_count_event = _create_calendar_event_from_text(text)

    if appex.is_running_extension():
        return _event_response(word_count_event)
    else:
        return _test_event_response(word_count_event)

def test_text():
    #text = _test_text_file()
    text = _test_text()
    _print_test(text)
    return text
    
    
###########################################
# Privates

def _get_credentials():
    store = ofile.Storage(CREDENTIAL_PATH)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + CREDENTIAL_PATH)
    return credentials

def _create_calendar_event_from_text(text):
    event_date = {"date": _get_date_from_text(text)}
    return {
        "end": event_date,
        "start": event_date,
        "summary": '%i Words' % _count_words(text)
    }

def _count_words(text):
    stripped_text = text.strip(string.punctuation)
    return len(stripped_text.split())

def _get_date_from_text(text):
    return text.splitlines()[0].lstrip('0 #')

def _get_calendarid():
    jsonfile = open(CALENDAR_CONFIG)
    calendar_id = json.load(jsonfile)['id']
    jsonfile.close()
    return calendar_id

def _create_events_api_object():
    credentials = _get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    return service.events()

def _event_response(event):
    events = _create_events_api_object()
    query = events.insert(calendarId=_get_calendarid(), body=event)
    return query.execute()

def _read_file(file_name):
    with open (file_name, 'r') as f:
        file_text = f.read()
    f.closed
    return file_text
    
def _test_event_response(event):
    import time
    time.sleep(3)
    print('Simulating test response')
    return event

def _test_text_file():
    print('Reading test text file')
    return _read_file(TEST_FILE)
    
def _test_text():
    from datetime import date
    print('Generating test text')
    hud_alert('Running with test data ...\n', 'success', 1)
    return ('# %s \n Lorem ipsum dolor sit amet, '
            'consectetur adipisicing elit, sed do eiusmod, '
            'tempor incididunt ut labore et dolore magna, '
            'words-with-hyphens should be separated, '
            'aliqua.' % date.today().strftime('%Y-%m-%d'))

def _print_test():
    print('*****************TEST TEXT STARTS')
    print('*********************************')
    print(text)
    print('*********************************')
    print('*****************TEST TEXT ENDS')
    
if __name__ == '__main__':
    main()