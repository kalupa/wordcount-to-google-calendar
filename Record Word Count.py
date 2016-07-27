#!python3
# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import
import argparse
import datetime
import httplib2
import json
import os
import string

# google modules
from googleapiclient import discovery
import oauth2client
from oauth2client import file as ofile
from oauth2client import client
from oauth2client import tools

# pythonista modules
import appex
import clipboard

# If modifying these scopes, delete your previously saved credentials
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'data/client_secret.json'
APPLICATION_NAME = 'Daily Word Count Logger'

def get_credentials():
    credential_path = ('data/credentials-calendar.json')
    store = ofile.Storage(credential_path)
    credentials = store.get()
    
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def count_words(text):    
    stripped_text = text.strip(string.punctuation)
    return len(stripped_text.split())
    
def get_date_from_text(text):
    return text.splitlines()[0].lstrip('0 #')

def get_calendarid():
    jsonfile = open('data/calendar.json')
    calendar_id = json.load(jsonfile)['id']
    jsonfile.close()
    return calendar_id

def create_calendar_event_from_text(text):
    event_date = {"date": get_date_from_text(text)}
    return {
        "end": event_date,
        "start": event_date,
        "summary": '%i Words' % count_words(text)
    }   
    
def create_events_api_object():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    return service.events()

def insert_daily_word_count_event(text):
    word_count_event = create_calendar_event_from_text(text)
    
    if appex.is_running_extension():
        events = create_events_api_object()
        query = events.insert(calendarId=get_calendarid(), body=word_count_event)
        return query.execute()
    else:
        return word_count_event

def get_text():
    if not appex.is_running_extension():
        print('This script is intended to be run from the sharing extension.')
        return
        #print('Running in Pythonista app, using test data...\n')
        #today = date.today().strftime('%Y-%m-%d')
        #text = '# %s \n Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.' % today
        #return text
    else:
        return appex.get_text()
            
def main():
    text = get_text()
    if text:
        result = insert_daily_word_count_event(text)
        print('Posted %s' % result['summary'], result['start']['date'])        
    else:
        print('No input text found.')

if __name__ == '__main__':
    main()
