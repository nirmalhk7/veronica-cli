from collections import defaultdict
from veronica.commands.email import do_email
from veronica.commands.calendar import do_calendar

def do_list(self,line):
    def do_new_error():
        print("Apologies, incorrect command.")
    subcommands= defaultdict(do_new_error,{
        "email": do_email,
        "calendar": do_calendar
    })
    if(line):
        subcommands[line.split(" ")[0]](self," ".join(line.split(" ")[1:]))
    else:
        do_new_error()