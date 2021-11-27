from random import randint

from sys import exit

def do_exit(self, args):
    self.do_EOF(args)

def do_EOF(self, line):
    self.output.print(self.intents["exit"][randint(0,len(self.intents["exit"])-1)].replace("<name>",self.username))
    exit(1)