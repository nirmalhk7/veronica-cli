from collections import defaultdict
from pathlib import Path
from veronica.config import unit
from veronica.voice import vx_print
from json import load
import inspect
import webbrowser
import re

@unit
def query(self,args):
    """
        
    """
    settings= load(open(Path.home()/"veronica.settings.json","r+"))[inspect.stack()[0][3][3:]]
    url_regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    def invalid_command():
        return "Invalid command. Try running 'help'"

    def query_get(key):
        if(" ".join(args[1:]) not in settings):
            vx_print("Sorry, wrong key.")
            return
        if(re.match(url_regex,settings[key])):
            webbrowser.open(settings[key])
            vx_print("Okay, I've opened that on your browser.")
        else:
            print(key)
        pass
    def query_list(key):
        for i in settings.keys():
            print("\t{}".format(i))
        pass
    def query_create(key):
        pass
    def query_update(key):
        pass
    def query_delete(key):
        pass
    print("")