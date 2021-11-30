"""Console script for veronica."""

from warnings import simplefilter

from veronica.user import User
simplefilter("ignore", category=DeprecationWarning)

import argparse
import json
from collections import defaultdict
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from cmd import Cmd
import getpass
import pkg_resources
import logging
from pathlib import Path
import pickle
from rich.console import Console
from veronica.voice import VoiceUtility
from rich.layout import Layout
from rich import print
from rich.progress import Progress
from subprocess import PIPE, run

import spacy





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
    user= User()
    
    console = Console()
    intents= json.loads(pkg_resources.resource_string(__name__,"/data/intents.json").decode("utf-8","ignore"))


    nlp=None
    synsets=None

    from veronica.commands.calc import do_calc
    from veronica.commands.info import do_info
    from veronica.commands.weather import do_weather
    from veronica.commands.email import do_email
    from veronica.commands.calendar import do_calendar
    from veronica.commands.search import do_search
    from veronica.commands.store import do_store
    from veronica.commands.exit import do_exit, do_EOF
    from veronica.commands.list import do_list
    from veronica.commands.reminders import do_remind
    from veronica.commands.meet import do_meet

    def __init__(self,silent=False):
        super().__init__()
        self.method_names=[i for i in dir(self) if i[:3]=="do_"]
        self.output= VoiceUtility(silent)
        with Progress(transient=True) as progress:
            t2= progress.add_task("[pink]Loading settings configurations...",start=False)
            with open(Path.home() / "veronica.settings.json", "r") as f:
                self.settings=json.load(f)
        if(silent):
            print("[gray][i]Running on silent mode ...[/][/]")
        
    
    def vx_os_output(self,command):
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        return result.stdout.strip()

    def vx_google_setup(self):
        creds = None
        if "token" in self.settings["google"]:
            creds = Credentials.from_authorized_user_info(
                self.settings["google"]["token"], self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        
            else:
                flow = InstalledAppFlow.from_client_config(
                    self.settings["google"]["credentials"], self.SCOPES)
                creds = flow.run_local_server(port=0)
            self.settings["google"]["token"] = json.loads(creds.to_json())
            with open(Path.home() / "veronica.settings.json", "w") as f:
                json.dump(self.settings, f, indent=4)
        return creds

    def cmdloop(self, intro) -> None:
        self.output.print(intro)
        super().cmdloop(intro="")

    def emptyline(self):
        return None

    def postcmd(self, stop: bool, line: str):
        # vx_empty_stack()
        pass
    
    def precmd(self, line):
        line_arr= line.split(" ")
        if "do_"+line_arr[0] in self.method_names:
            return line
        
        elif line in self.settings["commands"].keys():
            print(self.vx_os_output(self.settings["commands"][line]))
            return ""

        elif(not self.synsets and not self.nlp):
            with Progress(transient=True) as progress:
                t2= progress.add_task("[green]Loading ...",start=False)
                with open(pkg_resources.resource_filename(__name__,"/data/module.weights"), 'rb') as pickle_file:
                    self.synsets = pickle.load(pickle_file)
                with open(pkg_resources.resource_filename(__name__,"/data/en_core_web_md"), 'rb') as pickle_file:
                    self.nlp = pickle.load(pickle_file)
        
        line_nlp= self.nlp(line)
        max_similarity=-1
        max_similarity_command=None
        for i in self.synsets.keys():
            similarity= round(line_nlp.similarity(i),2)
            if(similarity>=0.75 and similarity>max_similarity):
                max_similarity=similarity
                max_similarity_command= self.synsets[i]


        if(max_similarity!=-1):
            return max_similarity_command+(" "+str(line_nlp.ents[0]) if line_nlp.ents else "")

        return line

    def do_version(self,line):
        layout = Layout(size=10)
        # TODO Build a good looking layout here.
        print(layout)
    
    def onecmd(self, line: str) -> bool:
        logging.debug("COMMAND "+line)
        return super().onecmd(line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', default=logging.DEBUG, help="Logging Level")
    parser.add_argument('-s','--silent',help="Run Veronica on silent mode.",action='store_true')
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

    prompt = Veronica(args.silent)
    prompt.prompt = 'veronica> '
    prompt.ruler = '='
    
    if (len(args._)): 
        getattr(prompt,"do_"+prompt.precmd(" ".join(args._)).strip())(" ".join(args._[1:]))
    else:
        prompt.cmdloop("Welcome {}! Veronica at your service ...".format(getpass.getuser().capitalize()))
    return 0

if __name__=="__main__":
    main()