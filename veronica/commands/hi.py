from random import randint


from veronica.voice import vx_print

from veronica.unit import unit

@unit(label=["Greetings","Hey"])
def do_hi(self,args):
    vx_print(self.intents["hi"][randint(0,len(self.intents["hi"])-1)].replace("<name>",self.username))