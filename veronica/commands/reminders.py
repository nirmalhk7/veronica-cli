from rich.table import Table
from rich.prompt import Prompt, Confirm
from veronica.unit import unit
from veronica.utils.reminders.reminders_client import RemindersClient
from datetime import date
from veronica.voice import vx_print
from dateutil import parser

def list_reminders(params):
    client= RemindersClient(params["SCOPES"])
    reminders = client.list_reminders(hours_upto=72)
    return reminders


def do_reminders(self,line):
    table = Table()
    table.add_column("Type")
    table.add_column("Title")
    table.add_column("Calendar")
    table.add_column("Duration")
    reminders= list_reminders({"SCOPES":self.SCOPES})
    for reminder in reminders:
        table.add_row(
            "Calendar",
            "[{}][link={}]{}[/link][/]".format(reminder["color"],
                                               reminder["link"], reminder["title"]),
            "[{}]{}[/]".format(reminder["color"], reminder["calendar"]),
            "[{}]{}[/]".format(reminder["color"], str(reminder["start"]))
        )
    self.console.print(table)

@unit(label="Set a reminder")
def do_remind(self,line):
    client= RemindersClient(self.SCOPES)
    dt= Prompt.ask("When do you want this to be reminded?",default=str(date.today()))
    dt= parser.parse(dt)
    print(self.ruler*50)
    print("Title: {}".format(line))
    print("Timestamp: {}\n".format(dt))
    if(Confirm.ask("Confirm?", default="y")):
        reminder = client.create_reminder(dt,line)
        if(reminder):
            vx_print("Duly noted.")
    return