from random import randint

from veronica.unit import unit

@unit(label=["Great work","I like you"])
def do_great(self, args):
    print(self.intents["great"][randint(0,len(self.intents["great"])-1)].replace("<name>",self.username))
