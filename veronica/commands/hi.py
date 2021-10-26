from random import randint

from veronica.voice import vx_print

def do_hi(self,args):
    response = ["Hey!",
        ""
        "Greetings "+self.username+", how can I help you?",
        "Good Morning "+self.username+", what can I do for you today?",
        "Veronica at your service, sir. What shall I do today?"
    ]
    vx_print(response[randint(0,len(response)-1)])