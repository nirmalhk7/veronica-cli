from json import dumps, load
from pathlib import Path
from typing import Type
from veronica.config import unit
from veronica.voice import vx_print
from googleapiclient.discovery import build
import os
from datetime import datetime, timedelta
from rich.table import Table
from rich import print


def do_calendar(self, args):
    """
        Print all events 72 hours ahead of current time.
    """

    creds = self.vx_google_setup()
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z'
    maxLimit = (datetime.utcnow() + timedelta(hours=72)).isoformat() + 'Z'

    calendars = service.calendarList().list().execute().get("items", [])
    events = []

    table= Table()
    table.add_column("Type")
    table.add_column("Title")
    table.add_column("Calendar")
    table.add_column("Duration")

    for calendar in calendars:
        if (calendar.get("selected", False) == True):
            cal_events = service.events().list(calendarId=calendar["id"],
                                               timeMin=now,
                                               timeMax=maxLimit,
                                               maxResults=2500).execute().get(
                                                   'items', [])
            for cal_event in cal_events:
                new_event = {
                    "link":
                    cal_event["htmlLink"],
                    "title":
                    cal_event["summary"],
                    "calendar":
                    calendar.get("summaryOverride", None)
                    or calendar.get("summary", None),
                    "color":
                    calendar["backgroundColor"]
                }

                
                # If date is present in start or end times, it means event is all day. So the same thing replicates
                # for end date as well.
                if ("date" in cal_event["start"]):
                    new_event["start"] = datetime.strptime(
                        cal_event['start']['date'], "%Y-%m-%d")
                    new_event["end"] = datetime.strptime(
                        cal_event['end']['date'], "%Y-%m-%d")
                else:
                    new_event['start'] = datetime.strptime(
                        cal_event["start"]["dateTime"].upper().split("+")[0].split("Z")
                        [0], "%Y-%m-%dT%H:%M:%S")
                    new_event['end'] = datetime.strptime(
                        cal_event['end']['dateTime'].upper().split("+")[0].split("Z")
                        [0], "%Y-%m-%dT%H:%M:%S")

                if ("hangoutLink" in cal_event):
                    new_event["hangoutLink"] = cal_event["hangoutLink"]
                events.append(new_event)
    events.sort(key=lambda x: x["start"], reverse=True)
    for i in events:
        table.add_row(
            "Event",
            "[{}][link={}]{}[/link][/]".format(i["color"],i["link"],i["title"]),
            "[{}]{}[/]".format(i["color"],i["calendar"]),
            "[{}]{}[/]".format(i["color"],str(i["start"]))
        )
    self.console.print(table)
