from random import randint
from veronica.config import unit
from veronica.voice import vx_print

@unit
def great(self, args):
    vx_print(self.intents["great"][randint(0,len(self.intents["great"])-1)].replace("ABC",self.username))