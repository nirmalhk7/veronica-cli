
from random import randint
from veronica.unit import unit


@unit(label="Tell me a joke")
def do_joke(self,args):
    self.output.print(self.intents["joke"][randint(0,len(self.intents["joke"])-1)])