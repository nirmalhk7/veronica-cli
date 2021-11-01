from json import dumps, load
from pathlib import Path
from typing import Type
from veronica.config import component
from veronica.voice import vx_print
from googleapiclient.discovery import build
import os
from datetime import datetime

@component
def do_calendar(self,args):
    def dateformat(inp):
        inp= inp.split("+")[0]
        return datetime.strptime(inp,"%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M")
    """
        Print upcoming 10 events from calendar.
    """
    try:
        creds = self.vx_google_setup(self,self.SCOPES)
    except TypeError:
        creds = self.vx_google_setup(self.SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    for i in events:
        start= i['start']['dateTime'].split("+")[0]
        start= datetime.strptime(start,"%Y-%d-%mT%H:%M:%S")
        end= i['end']['dateTime'].split("+")[0]
        end= datetime.strptime(end,"%Y-%d-%mT%H:%M:%S")
        print(f"{start.strftime('%-m %b, %-I:%M %p'): <30} {i['summary']: <60}")
    # print(events)