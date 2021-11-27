from random import randint






from veronica.unit import unit

@unit(label=["About you","Who are you"])
def do_intro(self, args):
    response = [
        "I'm Veronica, your personal Linux assistant.",
        "Heya " + self.username + ", I'm Veronica, your Linux assistant.",
        "I'm your personal Linux assistant Veronica. To know more about what I can do, please type 'help'."
    ]
    self.output.print(response[randint(0, len(response) - 1)])
