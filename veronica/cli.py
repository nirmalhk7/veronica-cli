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

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from cmd import Cmd
import getpass
import pkg_resources
from nltk import download
from nltk import word_tokenize
from nltk.corpus import stopwords, wordnet as wn
import logging
from pathlib import Path
import pickle
from rich.console import Console
from veronica.voice import vx_empty_stack, vx_speak
from rich.layout import Layout
from rich import print

download('wordnet', quiet=True)

stop_words = set(stopwords.words('english'))
try:
    synsets = dict(pickle.load(pkg_resources.resource_string(__name__,"/data/module.weights").decode("utf-8","ignore")))

except:
    synsets=[]


config_dictionary = {}
for pos, offset in synsets:
    config_dictionary[wn.synset_from_pos_and_offset(
        pos, offset)] = synsets[(pos, offset)]





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
    from veronica.commands.query import do_store
    from veronica.commands.exit import do_exit
    from veronica.commands.great import do_great
    from veronica.commands.list import do_list
    from veronica.commands.reminders import do_remind
    from veronica.commands.meet import do_meet
    

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

    def onecmd(self, line: str) -> bool:
        return super().onecmd(line)

    def do_version(self,line):
        layout = Layout(size=10)
        # TODO Build a good looking layout here.
        print(layout)

    def precmd(self, line):
        line = line.lower()
        search_query = line.split(" ")
        processed_search_query = []
        logging.debug("Removing stopwords ...")
        for token in search_query:
            if (token not in stop_words):
                processed_search_query.append(token)
        logging.debug("Preprocessed query: {}".format(
            " ".join(processed_search_query)))

        # If all words are stopwords, ignore :shrug:
        # But if the query term matches one of our unit names, then directly call
        if (not processed_search_query or "do_" + processed_search_query[0]
                in config_dictionary.values()):
            return " ".join(processed_search_query)

        logging.debug("Checking for similar words/ synonyms ...")
        usercmd_sysnets = wn.synsets(processed_search_query[0])
        similarity = {}
        for net in usercmd_sysnets:
            for v_cmd in config_dictionary.keys():
                similarity[(v_cmd, net)] = v_cmd.wup_similarity(net) or 0
        similarity_list = sorted(similarity,
                                 key=similarity.__getitem__,
                                 reverse=True)

        if (similarity_list and similarity[similarity_list[0]] > 0.75):
            max_similarity_key = similarity_list[0]
            command = config_dictionary[max_similarity_key[0]]
            logging.info("Max similarity: {} at {}".format(
                str(max_similarity_key), similarity[similarity_list[0]]))
            logging.debug("Reprocessed command: {}".format(command))
            try:
                # If command is passed as argument
                self.vx_setup(self)
                getattr(self,
                        "do_" + command)(self,
                                         " ".join(processed_search_query[1:]))
                vx_empty_stack()
            except TypeError:
                
                # If command is passed through Veronica CLI
                getattr(self,
                        "do_" + command)(" ".join(processed_search_query[1:]))
            except AttributeError:
                # If wrong command is passed with attributes.
                pass
            return ""
        else:
            return " ".join(processed_search_query)


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
        Veronica.precmd(Veronica, " ".join(args._))
    else:
        prompt.cmdloop("Welcome {}! Veronica at your service ...".format(getpass.getuser().capitalize()))
    return 0

if __name__=="__main__":
    main()