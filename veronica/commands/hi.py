from random import randint

def do_hi(self,args):
    response = ["Hey wassup!",
        "Konnichiwa "+self.username+"!",
        "Greetings "+self.username+", how can I help you?",
        "Good Morning "+self.username+", what can I do for you today?",
        "Veronica at your service, sir. What shall I do today?"
    ]
    print(args,response[randint(0,len(response)-1)])