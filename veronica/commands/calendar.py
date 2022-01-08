from json import dumps, load
from pathlib import Path
from typing import Type


from googleapiclient.discovery import build
from datetime import datetime, timedelta, date
from rich.table import Table
from rich import print
from rich.progress import Progress

from veronica.commands.reminders import list_reminders
from veronica.interfaces.event import EventInterface

from veronica.unit import unit


def list_birthdays(google_setup):
    service = build('people', 'v1', credentials=google_setup())
    birthday_arr = []
    d = service.people().connections().list(
        resourceName="people/me",
        personFields="birthdays,names").execute()
    birthday_arr += d["connections"]
    while "nextPageToken" in d:
        d = service.people().connections().list(
            resourceName="people/me",
            personFields="birthdays,names",
            pageToken=d["nextPageToken"]).execute()
        birthday_arr += d["connections"]
    events = []
    for contact in birthday_arr:
        if("birthdays" in contact):
            event = EventInterface(
                link="https://contacts.google.com/person/" +
                contact["resourceName"].split("/")[1],
                title="Birthday: " + contact["names"][0]["displayName"],
                calendar="Birthdays",
                color="red"
            )

            bday = contact["birthdays"][0]["date"]
            event.start = datetime(
                date.today().year,
                bday["month"],
                bday["day"]
            )
            event.end = event.start.replace(hour=23, minute=59)

            if(
                datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) <= event.start and
                event.end <= datetime.now() + timedelta(days=3)
            ):
                events.append(event)

    return events


def list_calendar(google_setup):
    service = build('calendar', 'v3', credentials=google_setup())

    now = datetime.utcnow().isoformat() + 'Z'
    maxLimit = (datetime.utcnow() + timedelta(days=3)).isoformat() + 'Z'

    calendars = service.calendarList().list().execute().get("items", [])
    events = []

    # TODO: Adjust for recurrrence, hangoutLink
    for calendar in calendars:
        if (calendar.get("selected", False)):
            cal_events = service.events().list(calendarId=calendar["id"],
                                               timeMin=now,
                                               timeMax=maxLimit,
                                               maxResults=2500).execute().get(
                                                   'items', [])

            for cal_event in cal_events:
                if("start" in cal_event):
                    event = EventInterface(
                        cal_event["htmlLink"],
                        cal_event["summary"] if "summary" in cal_event else "Untitled",
                        calendar.get(
                            "summaryOverride",
                            None) or calendar.get(
                            "summary",
                            None),
                        calendar["backgroundColor"])

                    event.set_date(cal_event['start'], cal_event['end'])

                    if ("hangoutLink" in cal_event):
                        event.hangoutLink = cal_event["hangoutLink"]

                    events.append(event)
    return events


@unit(label="Show me my calendar")
def do_calendar(self, args):
    """
        Print all events and reminders 72 hours ahead of current time.
    """

    table = Table()
    table.add_column("Title")
    table.add_column("Calendar")
    table.add_column("Start")
    # table.add_column("Duration")

    with Progress(transient=True) as progress:
        t1 = progress.add_task("[red]Loading calendars ...", start=False)
        events = list_calendar(self.vx_google_setup)
        t2 = progress.add_task("[yellow]Loading reminders ...", start=False)
        # events+= list_reminders({"SCOPES": self.SCOPES})
        t3 = progress.add_task("[#FFA500]Loading birthdays ...", start=False)
        events += list_birthdays(self.vx_google_setup)

        events.sort(key=lambda x: x.start, reverse=False)

        for i in events:
            table.add_row(
                "[{}][link={}]{}[/link][/]".format(i.color, i.link, i.title),
                "[{}]{}[/]".format(i.color, i.calendar),
                "[{}]{}[/]".format(i.color, str(i.start)),
                # "[{}]{}[/]".format(i.color, str(i.end-i.start))
            )

    self.output.print(
        table,
        speakMsg="There are {} things lined up in your calendar".format(
            len(events)))
