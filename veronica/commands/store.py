from collections import defaultdict
from pathlib import Path


from json import load
import inspect
import webbrowser
import re


def do_store(self,args):
    """
        Veronica inbuilt key value store.
    """

    url_regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if(args not in self.settings["store"].keys()):
        self.output.print("Invalid key specified: {}".format(args))
    
    if(re.match(url_regex,self.settings["store"][args])):
        webbrowser.open(self.settings["store"][args])
        self.output.print("Okay, I've opened that on your browser.")
    else:
        self.output.print(self.settings["store"][args],speak=False)