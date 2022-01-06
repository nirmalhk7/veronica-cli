"""Console script for veronica."""

import spacy
from subprocess import PIPE, run
from rich.progress import Progress
from rich import print
from rich.layout import Layout
from veronica.voice import VoiceUtility
from rich.console import Console
import pickle
from pathlib import Path
import logging
import pkg_resources
import getpass
from cmd import Cmd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from collections import defaultdict
import json
import argparse
from warnings import simplefilter

from veronica.interfaces.user import UserInterface
simplefilter("ignore", category=DeprecationWarning)


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
    user = UserInterface()
    console = Console()
    intents = json.loads(pkg_resources.resource_string(
        __name__, "/data/intents.json").decode("utf-8", "ignore"))
    settings = json.load(open(Path.home() / "veronica.settings.json", "r"))
    nlp = None
    synsets = None

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
    from veronica.commands.test import do_test

    def __init__(self, silent=False):
        super().__init__()
        self.method_names = [i for i in dir(self) if i[:3] == "do_"]
        self.output = VoiceUtility(silent)
        if(silent):
            print("[gray][i]Running on silent mode ...[/][/]")

    def vx_os_output(self, command):
        result = run(command, stdout=PIPE, stderr=PIPE,
                     universal_newlines=True, shell=True)
        return result.stdout.strip()

    def vx_google_setup(self):
        creds = None
        if "oauth_resp" in self.settings["google"]:
            creds = Credentials.from_authorized_user_info(
                self.settings["google"]["oauth_resp"], self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    self.settings["google"]["oauth"], self.SCOPES)
                creds = flow.run_local_server(port=0)

            self.settings["google"]["oauth_resp"] = json.loads(creds.to_json())
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
        line_arr = line.split(" ")
        if "do_" + line_arr[0] in self.method_names:
            return line

        elif "store" in self.settings and line in self.settings["store"].keys():
            return "store {}".format(line)

        elif(not self.synsets and not self.nlp):
            with Progress(transient=True) as progress:
                t2 = progress.add_task("[green]Loading ...", start=False)
                with open(pkg_resources.resource_filename(__name__, "/data/module.weights"), 'rb') as pickle_file:
                    self.synsets = pickle.load(pickle_file)
                with open(pkg_resources.resource_filename(__name__, "/data/en_core_web_md"), 'rb') as pickle_file:
                    self.nlp = pickle.load(pickle_file)

        line_nlp = self.nlp(line)
        max_similarity = -1
        max_similarity_command = None
        for i in self.synsets.keys():
            similarity = round(line_nlp.similarity(i), 2)
            if(similarity >= 0.75 and similarity > max_similarity):
                max_similarity = similarity
                max_similarity_command = self.synsets[i]

        if(max_similarity != -1):
            return max_similarity_command + \
                (" " + str(line_nlp.ents[0]) if line_nlp.ents else "")

        return line

    def do_version(self, line):
        layout = Layout(size=10)
        # TODO Build a good looking layout here.
        print(layout)

    def onecmd(self, line: str) -> bool:
        logging.debug("COMMAND " + line)
        super().onecmd(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l', '--log', default=logging.DEBUG, help="Logging Level")
    parser.add_argument(
        '-s', '--silent', help="First time setup", action='store_true')
    parser.add_argument(
        '-s',
        '--setup',
        help="Run Veronica on silent mode.",
        action='store_true')
    parser.add_argument(
        '_', nargs='*', help=", ".join([attr[3:] for attr in dir(Veronica) if attr[:3] == "do_"]))
    args = parser.parse_args()

    level = None
    if(args.log in logging._nameToLevel):
        level = logging._nameToLevel[args.log]

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=level or logging.DEBUG,
        filename=Path.home() / "veronica.log",
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.captureWarnings(True)

    prompt = Veronica(args.silent)
    prompt.prompt = 'veronica › '
    prompt.ruler = '='

    if (len(args._)):
        getattr(
            prompt,
            "do_" +
            prompt.precmd(
                " ".join(
                    args._)).strip().split(" ")[0])(
                " ".join(
                    args._))
    else:
        prompt.cmdloop("Welcome {}! Veronica at your service ...".format(
            UserInterface.system_username))
    return 0


if __name__ == "__main__":
    main()
