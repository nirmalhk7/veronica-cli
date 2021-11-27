
def do_calc(self, args):
    inpstr = args.split(' ')[0]
    self.output.print("Your result is {}".format(eval(inpstr)))
