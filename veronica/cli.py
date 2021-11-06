"""Console script for veronica."""
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
from veronica.config import units, unit

from veronica.voice import vx_empty_stack, vx_speak

for i in dir(unit):
    if(not i.startswith("__")):
        print(getattr(unit,i))

download('stopwords', quiet=True)
download('omw', quiet=True)
stop_words = set(stopwords.words('english'))
synsets = dict(
    pickle.load(
        pkg_resources.resource_stream(__name__,
                                      "data/command_synsets.veronica")))

config_dictionary = {}
for pos, offset in synsets:
    config_dictionary[wn.synset_from_pos_and_offset(
        pos, offset)] = synsets[(pos, offset)]


class Veronica(Cmd):
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/calendar.readonly',
        "https://www.googleapis.com/auth/drive.readonly"
    ]
    path = __name__
    env = defaultdict()  # or dict {}
    username = getpass.getuser().capitalize()
    console = Console()
    intents= json.loads(pkg_resources.resource_string(__name__,"/data/intents.json").decode("utf-8","ignore"))

    def vx_setup(self):
        with open(Path.home() / ".veronica.env") as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                key, value = line.strip().split('=')
                key, value = key.strip(), value.strip()
                value = int(value) if value.isdigit() else value
                self.env[key] = value

        logging.debug("Loaded env variables from {}".format(
            str(Path.home() / ".veronica.env")))

    def vx_google_setup(self, SCOPES):
        with open(Path.home() / "veronica.settings.json", "r") as f:
            settings = json.load(f)
        creds = None
        if "token" in settings["google"]:
            creds = Credentials.from_authorized_user_info(
                settings["google"]["token"], SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    settings["google"]["credentials"], SCOPES)
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

    def precmd(self, line, nonCli= False):
        line = line.lower()
        search_query = word_tokenize(line)
        processed_search_query = []
        logging.debug("Removing stopwords ...")
        for token in search_query:
            if (token not in stop_words):
                processed_search_query.append(token)
        logging.debug("Preprocessed query: {}".format(
            processed_search_query))

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
            logging.debug("Query parameters: {}".format(processed_search_query[1:]))
            if(nonCli):
                self.vx_setup(self)
                units[command](self, processed_search_query[1:])
                vx_empty_stack()
            else:
                units[command](self, processed_search_query[1:])

            
            # try:
            #     # If command is passed as argument
            #     self.vx_setup(self)
                
            #     getattr(self,"do_" + command).method(self," ".join(processed_search_query[1:]))
            #     vx_empty_stack()
            # except TypeError:
                
            #     # If command is passed through Veronica CLI
            #     getattr(self,
            #             "do_" + command).method(" ".join(processed_search_query[1:]))
            # except AttributeError:
            #     # If wrong command is passed with attributes.
            #     pass
            return ""
        else:
            return " ".join(processed_search_query)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', default=logging.DEBUG, help="Logging Level")
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
        level=level or logging.ERROR)
    prompt = Veronica()
    prompt.prompt = 'veronica> '
    prompt.ruler = '-'

    if (len(args._)):
        Veronica.precmd(Veronica, " ".join(args._), True)
    else:
        prompt.cmdloop("Welcome {}! Veronica at your service ...".format(getpass.getuser().capitalize()))
    return 0