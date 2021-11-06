from random import randint
from veronica.voice import vx_print

def do_exit(self, args):
    vx_print(self.intents["exit"][randint(0,len(self.intents["hi"])-1)].replace("<name>",self.username))
    exit()