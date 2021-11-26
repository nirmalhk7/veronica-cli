from pathlib import Path
import json
from random import randint
import webbrowser
from veronica.voice import vx_print


def do_meet(self,line):
    """
        Generate a Google Meet URL and open it on the browser.
        USAGE:
            veronica> meet
            Meet link has been copied to the clipboard. Opening the same in your browser ...
    """
    
    with open(Path.home() / "veronica.settings.json", "r") as f:
        meets = json.load(f)["google"]["meet"]
    vx_print("Meet link has been copied to the clipboard. Opening the same in your browser ...")
    webbrowser.open(meets[randint(0,len(meets)-1)])