from collections import deque 
from os import system
from rich import print


print_stack= deque()
def vx_print(arg, color="", speak=True, speakText=None):
    if(speak and not speakText):
        print_stack.append(str(arg))
    elif(speak and speakText):
        print_stack.append(str(speakText))
    print(color+arg)

def vx_speak(speak_str):
    system('espeak "'+speak_str+'" -ven-us+m2')

def vx_empty_stack():
    while print_stack:
        vx_speak(print_stack.popleft())