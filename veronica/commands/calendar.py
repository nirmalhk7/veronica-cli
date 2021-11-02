from json import dumps, load
from pathlib import Path
from typing import Type
from veronica.config import component
from veronica.voice import vx_print
from googleapiclient.discovery import build
import os
from datetime import datetime, timedelta

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

    now = datetime.utcnow().isoformat() + 'Z'
    maxLimit= (datetime.utcnow()+timedelta(hours=72)).isoformat() + 'Z'

    calendars= service.calendarList().list().execute().get("items",[])
    events=[]
    for calendar in calendars:
        if(calendar.get("selected",False)==True):
            cal_events= service.events().list(calendarId=calendar["id"], timeMin=now, timeMax= maxLimit,
                                            maxResults=2500).execute().get('items',[])
            for cal_event in cal_events:
                new_event={
                    "link": cal_event["htmlLink"],
                    "title": cal_event["summary"],
                    "calendar": calendar.get("summaryOverride",None) or calendar.get("summary",None),
                    "color": calendar["backgroundColor"]
                }

                # If date is present in start or end times, it means event is all day. So the same thing replicates
                # for end date as well.
                if("date" in cal_event["start"]):
                    new_event["start"]=datetime.strptime(cal_event['start']['date'],"%Y-%m-%d")
                    new_event["end"]=datetime.strptime(cal_event['end']['date'],"%Y-%m-%d")
                else:
                    new_event['start']=datetime.strptime(cal_event["start"]["dateTime"].split("+")[0],"%Y-%m-%dT%H:%M:%S")
                    new_event['end']= datetime.strptime(cal_event['end']['dateTime'].split("+")[0],"%Y-%m-%dT%H:%M:%S")

                if("hangoutLink" in cal_event):
                    new_event["hangoutLink"]=cal_event["hangoutLink"]
                events.append(new_event)                  
    events.sort(key=lambda x:x["start"], reverse=True)
    print(events)
