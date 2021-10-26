from collections import deque 
from os import system
import re

print_stack= deque()
def vx_print(arg, color="", speak=True):
    if(speak):
        print_stack.append(str(arg))
    print(color+arg)

def vx_speak(speak_str):
    system('espeak "'+speak_str+'" -ven-us+m2')

def vx_empty_stack():
    while print_stack:
        vx_speak(print_stack.popleft())