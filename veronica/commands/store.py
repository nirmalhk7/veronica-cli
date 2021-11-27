from collections import defaultdict
from pathlib import Path


from json import load
import inspect
import webbrowser
import re


def do_store(self,args):
    """
        Veronica inbuilt key value store.
        USAGE:
        > store [list|create|delete|update]    
    """

    url_regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    def invalid_command():
        return "Invalid command. Try running 'help'"

    def store_get(key):
        if(" ".join(args[1:]) not in settings):
            print("Sorry, wrong key.")
            return
        if(re.match(url_regex,settings[key])):
            webbrowser.open(settings[key])
            print("Okay, I've opened that on your browser.")
        else:
            print(key)
        pass
    def store_list(key):
        for i in settings.keys():
            print("\t{}".format(i))
        pass
    def store_create(key):
        pass
    def store_update(key):
        pass
    def store_delete(key):
        pass
    print("")