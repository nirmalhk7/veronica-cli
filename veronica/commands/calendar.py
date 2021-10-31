from json import dumps, load
from pathlib import Path
from typing import Type
from veronica.config import component
from veronica.voice import vx_print
from googleapiclient.discovery import build
import os
import datetime


@component
def do_calendar(self,args):
    """
        Print upcoming 10 events from calendar.
    """
    try:
        creds = self.vx_google_setup(self,self.SCOPES)
    except TypeError:
        creds = self.vx_google_setup(self.SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    print(events)