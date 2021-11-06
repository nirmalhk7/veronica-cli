from random import randint
from veronica.voice import vx_print

def do_great(self, args):
    vx_print(self.intents["great"][randint(0,len(self.intents["great"])-1)].replace("<name>",self.username))