from collections import deque 
from os import system
import time
import random
import subprocess
from threading import Timer
from functools import partial
from rich import print

class VoiceUtility():
    # Special thanks to @Darkonaut https://stackoverflow.com/questions/52786288/python-running-code-simultaneously-tts-and-print-functions

    speak_stack=[]
    def _espeak(self,msg):
        cmd = ["espeak", '-s130', '-ven+f5', msg]
        subprocess.run(cmd)
    
    def speak(self,response,responsetts=None, interval=0):
        if responsetts is not None:
            response = responsetts
        Timer(interval=interval, function=self._espeak, args=(response,)).start()

    def print(self,msg,speakMsg=False,speak=True):
        time.sleep(random.uniform(0.5, 2))
        print(msg)
        if(speakMsg):
            self.speak(speakMsg)
        elif(speak):
            self.speak(msg)
        
