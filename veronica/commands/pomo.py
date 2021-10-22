from cmd import Cmd
import os
import random
import getpass
import tkinter as t
import time

class Countdown():
    def __init__(self):
        self.hour=0
        self.minute=0
        self.second=0
    
    def setTime(self,seconds: int):
        self.second=seconds%60
        seconds-=seconds%60
        self.hour=seconds//60//60
        self.minute=seconds//60-self.hour*60

    def __str__(self):
        return "{}:{}:{}".format(self.hour,self.minute,self.second)  

class Pomodoro(Cmd):
    def do_pomo(self,args):
        def closewin():
            root.destroy()
        root=t.Tk()
        root.attributes("-fullscreen",True)
        root['bg']='#444444'
        root.title('Pomodoro Manager')
        var=t.StringVar()
        var.set("Text")
        label = t.Label( root, textvariable=var, relief=t.RAISED, bd=0,fg='white',font=("Arial", 200),background='#444444')
        start = time.time()
        time.perf_counter()
        cd=Countdown()    
        elapsed = 0

        # print("END")
        # root.bind("<Button-1>",closewin())
        label.pack()

        root.mainloop()
        while elapsed < 20:
            # print(int(time.time()-start),seconds)
            elapsed=int(time.time()-start)
            cd.setTime(20-elapsed)
            var.set(cd)
            # print("seconds count: %d" % (time.time()-start)) 
            time.sleep(1)  
        