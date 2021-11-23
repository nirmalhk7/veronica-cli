from collections import defaultdict
from veronica.commands.reminders import new_reminder

def do_new(self,line):
    print(line)
    def do_new_error():
        print("Apologies, incorrect command.")
    subcommands= defaultdict(do_new_error,{
        "reminder": new_reminder
    })
    if(line):
        subcommands[line.split(" ")[0]](self," ".join(line.split(" ")[1:]))
    else:
        do_new_error()