from rich.table import Table
from veronica.utils.reminders.reminders_client import RemindersClient

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