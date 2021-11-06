from random import randint
from veronica.config import unit

from veronica.voice import vx_print

@unit(synonyms=["hey","yo"])
def hi(self,args):
    vx_print(self.intents["hi"][randint(0,len(self.intents["hi"])-1)].replace("ABC",self.username))