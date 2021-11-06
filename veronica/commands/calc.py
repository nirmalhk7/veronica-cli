from veronica.config import unit


@unit
def calc(self, args):
    inpstr = args.split(' ')[0]
    print("Your result is", eval(inpstr))
