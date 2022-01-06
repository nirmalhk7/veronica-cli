
from os import stat_result
from datetime import date, datetime, timedelta


class EventInterface():
    link = None
    title = "Untitled"
    calendar = None
    color = None
    hangoutLink = None
    start = None
    end = None

    def set_date(self, start, end):
        if("date" in start):
            self.start = datetime.strptime(start['date'], "%Y-%m-%d")
            self.end = datetime.strptime(end['date'], "%Y-%m-%d")
        else:
            self.start = datetime.strptime(
                start["dateTime"].upper().split("+")[0].split("Z")[0],
                "%Y-%m-%dT%H:%M:%S")
            self.end = datetime.strptime(
                end["dateTime"].upper().split("+")[0].split("Z")[0],
                "%Y-%m-%dT%H:%M:%S")

    def __init__(self, link, title, calendar, color) -> None:
        self.link = link
        self.title = title
        self.calendar = calendar
        self.color = color
