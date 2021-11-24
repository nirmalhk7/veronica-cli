from collections import defaultdict
from veronica.commands.reminders import list_reminders

def do_new(self,line):
    print(line)
    def do_new_error():
        print("Apologies, incorrect command.")
    subcommands= defaultdict(do_new_error,{
        "reminder": list_reminders
    })
    if(line):
        subcommands[line.split(" ")[0]](self," ".join(line.split(" ")[1:]))
    else:
        do_new_error()