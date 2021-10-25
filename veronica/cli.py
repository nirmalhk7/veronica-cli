"""Console script for veronica."""
import argparse
import sys
from collections import defaultdict
from pip._vendor.colorama import init
from pip._vendor.colorama import Fore
from cmd import Cmd
import getpass
import pkg_resources
from nltk import download
from nltk import word_tokenize
from nltk.corpus import stopwords, wordnet as wn
import logging
from pathlib import Path
import pickle
from os import getenv
from dotenv import load_dotenv




parser = argparse.ArgumentParser()
parser.add_argument('_', nargs='*')
parser.add_argument('-l','--log',default=logging.DEBUG,help="Logging Level")
args = parser.parse_args()

level= None
if(args.log=="CRITICAL"):
    level= logging.CRITICAL
elif(args.log=="ERROR"):
    level= logging.ERROR
elif(args.log=="WARNING"):
    level= logging.WARNING
elif(args.log=="INFO"):
    level= logging.INFO
elif(args.log=="DEBUG"):
    level= logging.DEBUG
elif(args.log=="NOTSET"):
    level= logging.NOTSET
logging.basicConfig(level=level or logging.ERROR,filename=Path.home()/"veronica.log")


download('stopwords', quiet=True)
download('omw',quiet=True)
stop_words = set(stopwords.words('english'))
synsets = dict(pickle.load(pkg_resources.resource_stream(__name__,"data/command_synsets.veronica")))

config_dictionary={}
for pos,offset in synsets:
    config_dictionary[wn.synset_from_pos_and_offset(pos,offset)]=synsets[(pos,offset)]

class Veronica(Cmd):
    
    from veronica.commands.calc import do_calc
    from veronica.commands.hi import do_hi
    from veronica.commands.info import do_info
    from veronica.commands.intro import do_intro
    from veronica.commands.joke import do_joke
    from veronica.commands.weather import do_weather

    def cmdloop(self, intro) -> None:
        self.env = defaultdict() # or dict {}
        self.username = getpass.getuser().capitalize()
        with open(Path.home()/".veronica.env") as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                key, value = line.strip().split('=')
                key, value = key.strip(), value.strip()
                value= int(value) if value.isdigit() else value
                self.env[key]=value
        logging.debug("Loaded env variables from {}: {}".format(str(Path.home()/".veronica.env"),str(self.env)))
        return super().cmdloop(intro=intro)

    def emptyline(self):
        return None
    def precmd(self, line):
        line = line.lower()
        search_query= word_tokenize(line);
        processed_search_query=[]
        for token in search_query:
            if(token not in stop_words):
                processed_search_query.append(token)
        logging.debug("Preprocessed query: {}".format(" ".join(processed_search_query)))
        
        if(not processed_search_query):
            return " ".join(processed_search_query)

        if("do_"+" ".join(processed_search_query) in config_dictionary.values()):
            return " ".join(processed_search_query)

        usercmd_sysnets= wn.synsets(processed_search_query[0])
        similarity={}
        for net in usercmd_sysnets:
            for v_cmd in config_dictionary.keys():
                similarity[(v_cmd,net)]=v_cmd.wup_similarity(net) or 0
        similarity_list=sorted(similarity, key=similarity.__getitem__, reverse=True)
        
        if(similarity_list and similarity[similarity_list[0]]>0.85):
            max_similarity_key=similarity_list[0]
            command=config_dictionary[max_similarity_key[0]]
            logging.info("Max similarity: {} at {}".format(str(max_similarity_key),similarity[similarity_list[0]]))
            logging.debug("Reprocessed command: {}".format(command))
            
            try:
                getattr(self,"do_"+command)(" ".join(processed_search_query[1:]))
            except:
                getattr(self,"do_"+command)(self," ".join(processed_search_query[1:]))
            return ""
        else: 
            return " ".join(processed_search_query)

    




def main():
    """Console script for veronica."""
    # sentry_sdk.init("https://3ac0bcf6b7c94dceba16841163e807d0@o410546.ingest.sentry.io/5299322")

    init(autoreset=True)
    prompt = Veronica()
    prompt.prompt = 'veronica> '
    prompt.ruler = '-'

    if(len(args._)): 
        Veronica.precmd(Veronica," ".join(args._))
    else:
        prompt.cmdloop(Fore.YELLOW+'Welcome '+getpass.getuser().capitalize()+"! Veronica at your service ...")
    return 0


if __name__ == "__main__":
    print("Main")
    sys.exit(main())
