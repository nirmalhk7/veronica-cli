
from random import randint
from veronica.config import unit
from veronica.voice import vx_print

@unit()
def joke(self,args):
    vx_print(self.intents["joke"][randint(0,len(self.intents["joke"])-1)])