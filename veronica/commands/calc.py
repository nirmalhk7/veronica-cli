
def do_calc(self,args):
    inpstr = args.split(' ')[0]
    for x in inpstr:
        if(x.isalpha() and x!='e'):
            print("Sorry incorrect");
            return
    print("Your result is",eval(inpstr))
