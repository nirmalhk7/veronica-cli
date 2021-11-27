from random import randint




from veronica.unit import unit

@unit(label=["Greetings","Hey"])
def do_hi(self,args):
    self.output.print(self.intents["hi"][randint(0,len(self.intents["hi"])-1)].replace("<name>",self.username))