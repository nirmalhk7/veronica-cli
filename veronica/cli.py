"""Console script for veronica."""

import warnings
warnings.simplefilter("ignore", category=DeprecationWarning)

import argparse
import json
import sys
from collections import defaultdict
from typing import Type
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import spacy
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from cmd import Cmd
import getpass
import pkg_resources
import logging
from pathlib import Path
import pickle
from rich.console import Console
from veronica.voice import vx_empty_stack, vx_speak
from rich.layout import Layout
from rich import print
from rich.progress import Progress

with Progress(transient=True) as progress:
    t2= progress.add_task("[orange]Starting up ...",start=False)
    # download('wordnet', quiet=True)

    with open(pkg_resources.resource_filename(__name__,"/data/module.weights"), 'rb') as pickle_file:
        synsets = pickle.load(pickle_file)
    nlp= pickle.load(open("veronica/data/en_core_web_md","rb"))



class Veronica(Cmd):
    SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/contacts.readonly",
    "https://www.googleapis.com/auth/profile.language.read",
    "https://www.googleapis.com/auth/user.addresses.read",
    "https://www.googleapis.com/auth/user.birthday.read",
    "https://www.googleapis.com/auth/user.emails.read",
    "https://www.googleapis.com/auth/user.phonenumbers.read",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
    ]
    path = __name__
    env = defaultdict()  # or dict {}
    username = getpass.getuser().capitalize()
    console = Console()
    intents= json.loads(pkg_resources.resource_string(__name__,"/data/intents.json").decode("utf-8","ignore"))

    from veronica.commands.calc import do_calc
    from veronica.commands.hi import do_hi
    from veronica.commands.info import do_info
    from veronica.commands.intro import do_intro
    from veronica.commands.joke import do_joke
    from veronica.commands.weather import do_weather
    from veronica.commands.email import do_email
    from veronica.commands.calendar import do_calendar
    from veronica.commands.search import do_search
    from veronica.commands.store import do_store
    from veronica.commands.exit import do_exit, do_EOF
    from veronica.commands.great import do_great
    from veronica.commands.list import do_list
    from veronica.commands.reminders import do_remind
    from veronica.commands.meet import do_meet

    def __init__(self):
        super().__init__()
        self.method_names=[i for i in dir(self) if i[:3]=="do_"]

    def vx_setup(self):
        with open(Path.home() / ".veronica.env") as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                key, value = line.strip().split('=')
                key, value = key.strip(), value.strip()
                value = int(value) if value.isdigit() else value
                self.env[key] = value

        logging.debug("Loaded env variables from {}: {}".format(
            str(Path.home() / ".veronica.env"), str(self.env)))

    def vx_google_setup(self):
        with open(Path.home() / "veronica.settings.json", "r") as f:
            settings = json.load(f)
        creds = None
        if "token" in settings["google"]:
            creds = Credentials.from_authorized_user_info(
                settings["google"]["token"], self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        
            else:
                flow = InstalledAppFlow.from_client_config(
                    settings["google"]["credentials"], self.SCOPES)
                creds = flow.run_local_server(port=0)
            settings["google"]["token"] = json.loads(creds.to_json())
            with open(Path.home() / "veronica.settings.json", "w") as f:
                settings = json.dump(settings, f, indent=4)
        return creds

    def cmdloop(self, intro) -> None:
        self.vx_setup()
        # vx_speak('Welcome {}! Veronica at your service ...'.format(getpass.getuser().capitalize()))
        super().cmdloop(intro=intro)

    def emptyline(self):
        return None

    def postcmd(self, stop: bool, line: str):
        vx_empty_stack()
    
    def precmd(self, line):
        line_arr= line.split(" ")
        if "do_"+line_arr[0] in self.method_names:
            return line
        
        line_nlp= nlp(line)
        similar_unit_arr=[]
        for i in synsets.keys():
            similarity= round(line_nlp.similarity(i),2)
            if(similarity>=0.75):
                similar_unit_arr.append((synsets[i],similarity))
        similar_unit_arr=sorted(similar_unit_arr, key=lambda item: item[1],reverse=True)
        logging.debug("Query: {} Similarity Map: {}".format(line,similar_unit_arr))
        if(similar_unit_arr):
            return similar_unit_arr[0][0]
        return line

    def onecmd(self, line: str) -> bool:
        return super().onecmd(line)

    def do_version(self,line):
        layout = Layout(size=10)
        # TODO Build a good looking layout here.
        print(layout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', default=logging.DEBUG, help="Logging Level")
    parser.add_argument('-v','--version',help="Know more about Veronica",action='store_true')
    parser.add_argument('_', nargs='*',help=", ".join([attr[3:] for attr in dir(Veronica) if attr[:3]=="do_"]))
    args = parser.parse_args()

    level = None
    if (args.log == "CRITICAL"):
        level = logging.CRITICAL
    elif (args.log == "ERROR"):
        level = logging.ERROR
    elif (args.log == "WARNING"):
        level = logging.WARNING
    elif (args.log == "INFO"):
        level = logging.INFO
    elif (args.log == "DEBUG"):
        level = logging.DEBUG
    elif (args.log == "NOTSET"):
        level = logging.NOTSET

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=level or logging.DEBUG, 
        filename=Path.home()/"veronica.log",
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.captureWarnings(True)

    prompt = Veronica()
    prompt.prompt = 'veronica> '
    prompt.ruler = '='
    
    if (len(args._)): 
        getattr(prompt,"do_"+prompt.precmd(" ".join(args._)).strip())(" ".join(args._[1:]))
    else:
        prompt.cmdloop("Welcome {}! Veronica at your service ...".format(getpass.getuser().capitalize()))
    return 0

if __name__=="__main__":
    main()