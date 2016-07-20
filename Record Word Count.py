#!python3
# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import
import httplib2
import os

from googleapiclient import discovery
import oauth2client
from oauth2client import file as ofile
from oauth2client import client
from oauth2client import tools

import datetime
import string
import json
import appex
import clipboard

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'data/client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    
    credential_path = ('data/credentials-calendar.json')
    store = ofile.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def countwords(text):    
    stripped_text = text.strip(string.punctuation)
    words = stripped_text.split()
    return len(words)
    
def getdatefromtext(text):
    return text.splitlines()[0].lstrip('0 #')

def getcalendarid():
    jsonfile = open('data/calendar.json')
    calid = json.load(jsonfile)['id']
    jsonfile.close()
    return calid

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    
    if not appex.is_running_extension():
        print('This script is intended to be run from the sharing extension.')
        return
        #print('Running in Pythonista app, using test data...\n')
        #text = '# 02016-07-19\n Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    else:
        text = appex.get_text()
    
    if text:
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        
        date_for_count = {"date": getdatefromtext(text)}
        new_event = {
            "end": date_for_count,
            "start": date_for_count,
            "summary": '%i Words' % countwords(text)
        }
        events = service.events()
        query = events.insert(calendarId=getcalendarid(), body=new_event)
        result = query.execute()
        
        print('Posted %s' % result.get('summary'), result['start']['date'])
        
    else:
        print('No input text found.')


if __name__ == '__main__':
    main()
