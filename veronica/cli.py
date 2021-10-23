"""Console script for veronica."""
import argparse
import sys
from pip._vendor.colorama import init
from pip._vendor.colorama import Fore
from cmd import Cmd
import getpass
from .commands.information import Information
from .commands.friendly import Friendly
import pkg_resources
import sentry_sdk
from sentry_sdk import capture_message
from .commands.pomo import Pomodoro
from nltk import download
from nltk import word_tokenize
from nltk.corpus import stopwords, wordnet
from inspect import ismethod

download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

class Veronica(Friendly,Information,Pomodoro):
    # def do_EOF(self, args):
    #     print("")
    #     raise SystemExit

    # def emptyline(self):
    #     return True
    
    def direct(arg):
        print(arg,globals())
        globals()["Veronica"]["do_"+arg[0]](arg[1])

    def do_version(self,args):

        message=["Veronica v"+pkg_resources.require("veronica")[0].version,
        "Inspired from Tony Stark and built by Nirmal Khedkar",
        "Check out:",
        "   www.github.com/nirmalhk7/veronica-cli",             # TODO Display this as clickable link
        "   nirmallhk7.tech",                                   # TODO Display this as clickable link
        ""
        "Always #TeamIronMan. Love you 3000!"]
        xlen = 0
        for msg in message:
            if(xlen<len(msg)):
                xlen = len(msg)
        print("")
        print(Cmd.ruler*xlen)
        print("")
        for msg in message:
            print(msg)
        print("")
        print(Cmd.ruler*xlen)
    
    def onecmd(self, line):
        search_query= word_tokenize(line);
        processed_search_query=[]
        for token in search_query:
            if(token not in stop_words):
                processed_search_query.append(token)
        
        allcmds=[i[3:] for i in dir(self) if ismethod(getattr(self,i)) and i[:3]=="do_"]
        usercmd= wordnet.synsets(processed_search_query[0])
        if(usercmd):
            for allcmd in allcmds:
                allcmd_synsets= wordnet.synsets(allcmd)
                if(allcmd_synsets):
                    print(processed_search_query[0],allcmd,usercmd[0].wup_similarity(allcmd_synsets[0]))
        
        self.do_hi(processed_search_query[1:])
        # Get all relevant function names from this next line.
        # [i for i in dir(self) if ismethod(getattr(self,i)) and i[:3]=="do_"]
        

    def postloop(self):
        print("Thank you!")

def argParse(argx):
    Veronica.direct(argx);

def main():
    """Console script for veronica."""
    # sentry_sdk.init("https://3ac0bcf6b7c94dceba16841163e807d0@o410546.ingest.sentry.io/5299322")

    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()
    init(autoreset=True)
    prompt = Veronica()
    prompt.prompt = 'veronica> '
    prompt.ruler = '-'
    if(len(args._)): argParse(args._)
    prompt.cmdloop(Fore.YELLOW+'Welcome '+getpass.getuser().capitalize()+"! Veronica at your service ...")
    return 0


if __name__ == "__main__":
    print("Main")
    sys.exit(main())
