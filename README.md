# wordcount-to-google-calendar

Proof of concept for a simple little utility to allow me to send daily morning pages word counts to a google calendar of my choice. Mostly so I can see my writing streaks but also fun to experiment with the Google APIs and possibly App Engine at some point.

I've cribbed code from [NodeJS Quickstart](https://developers.google.com/google-apps/calendar/quickstart/nodejs) and [Python Quickstart](https://developers.google.com/google-apps/calendar/quickstart/python) to use as starting points.

## Worklog
### 2016-07-17
So far this is just a heavily modified version of the sample code from the Google App Calendar API documentation. It works to take in word count and date for the NodeJS version as command line arguments. Why reinvent the wheel when unix tools exist to do the hard bits? Using `wc`, `sed` and `xargs` does the annoying bits so the JS code can focus on the parts that aren't, for me, as easy to do in a shell script.

### 2016-07-18 
Sadly there's not really a simple way to run the JS code as it exists here on iOS without basically building an entire iOS app in phonegap. Seems like overkill for a simple utility.
Tested the "read" from calendar api in Python. I'm interested in getting the this working with Pythonista so I can just run the script as a "share sheet" on iOS. I've found a way to install `pip` modules in it but I'm getting a runtime error when it runs that looks like it's a problem with load paths for the modules. Not experienced enough with Python to know quickly how to fix it. Will return to see if I can muddle it out later.

### 2016-07-19
Managed to get the python to work. Not really 100% of the time, sometimes when it's doing the oauth setup it fails to properly detect that it can't open a web browser with the oauth2 client. That's fine, usually running it again will prompt for the token via a manual request. It now posts hard-coded data into the default calendar! I'll merge a wordcounter with this and then be able to run it from the share sheet and post into the correct calendar. I wonder how I can safely store the calendar id somewhere other than the source code itself.
