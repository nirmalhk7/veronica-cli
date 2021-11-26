from random import randint
from veronica.voice import vx_print
from sys import exit

def do_exit(self, args):
    self.do_EOF(args)

def do_EOF(self, line):
    vx_print(self.intents["exit"][randint(0,len(self.intents["exit"])-1)].replace("<name>",self.username))
    exit(1)