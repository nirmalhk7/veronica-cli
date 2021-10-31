from json import dumps, load
from pathlib import Path
from veronica.config import component
from veronica.voice import vx_print
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import datetime
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']



@component
def do_calendar(self,args):
    """
        Print upcoming 10 events from calendar.
    """
    settings= load(open(Path.home()/"veronica.settings.json","r+"))
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if "token" in settings["google"]:
        creds= Credentials.from_authorized_user_info(settings["google"]["token"], SCOPES)
        # creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow= InstalledAppFlow.from_client_config(settings["google"]["credentials"],SCOPES)
            # flow = InstalledAppFlow.from_client_secrets_file(
            #     'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        settings["google"]["token"]=creds.to_json();
        dumps(settings, indent = 4)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    pass