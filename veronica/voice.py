import logging
import time
import random
import subprocess
from threading import Timer
from rich import print
from gtts import gTTS
import os
import re
from pydub import AudioSegment, playback

FNULL = open(os.devnull, 'w')
_subprocess_call = playback.subprocess.call
playback.subprocess.call = lambda cmd: _subprocess_call(cmd, stdout=FNULL, stderr=subprocess.STDOUT)
class VoiceUtility():
    
    def __init__(self,silent) -> None:
        self.silent=silent    

    def remove_ansi_escape_seq(text):
        if text:
            text = re.sub(r'''(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]''', '', text)
        return text

    speak_stack=[]
    def _espeak(self,msg):
        try:
            tts = gTTS(text=msg, lang='en')
            filename = ".veronica.temp.mp3"
            tts.save(filename)
            playback.play(AudioSegment.from_mp3(filename))
            os.remove(filename)
        except Exception as e:
            logging.error(str(e))
            print(3)
            cmd = ["espeak", '-s130', '-ven+f5', msg]
            subprocess.run(cmd)
    
    def speak(self,response,responsetts=None, interval=0):
        if responsetts is not None:
            response = responsetts
        # Special thanks to @Darkonaut https://stackoverflow.com/questions/52786288/python-running-code-simultaneously-tts-and-print-functions
        Timer(interval=interval, function=self._espeak, args=(response,)).start()

    def print(self,msg,speakMsg=False,speak=True):
        time.sleep(random.uniform(0.5, 2))
        print(msg)
        if(speakMsg and not self.silent):
            self.speak(speakMsg)
        elif(speak and not self.silent):
            self.speak(msg)
        
