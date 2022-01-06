from collections import defaultdict
from veronica.commands.email import do_email
from veronica.commands.calendar import list_calendar
from veronica.commands.reminders import list_reminders


def do_list(self, line):
    def do_new_error():
        self.output.print("Apologies, incorrect command.", speak=False)
    subcommands = defaultdict(do_new_error, {
        "emails": do_email,
        "calendar": list_calendar,
        "reminders": list_reminders
    })
    if(line):
        subcommands[line.split(" ")[0]](self, " ".join(line.split(" ")[1:]))
    else:
        do_new_error()
