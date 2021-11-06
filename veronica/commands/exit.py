from random import randint
from veronica.config import unit
from veronica.voice import vx_print

@unit
def exit(self, args):
    vx_print(self.intents["exit"][randint(0,len(self.intents["hi"])-1)].replace("ABC",self.username))
    exit()