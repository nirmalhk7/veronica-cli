from veronica.voice import vx_print

def do_calc(self,args):
    inpstr = args.split(' ')[0]
    print("Your result is",eval(inpstr))
