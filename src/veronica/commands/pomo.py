from cmd import Cmd
import os
import random
import getpass
import tkinter as t
import time

class Pomodoro(Cmd):
    def do_pomo(self,args):
        root=t.Tk()
        root.attributes("-fullscreen",True)
        root['bg']='#444444'
        root.title('Pomodoro Manager')
        
        # text=t.Text(root,time.strftime("%H:%M:%S"),width=10).pack()

        root.mainloop()

        