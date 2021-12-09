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
    
    # TODO Detect for links
    print(1,args)