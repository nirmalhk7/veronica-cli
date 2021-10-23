"""Console script for veronica."""
import argparse
from collections import defaultdict
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
from nltk import download
from nltk import word_tokenize
from nltk.corpus import stopwords, wordnet
from inspect import ismethod
import logging
import json
import itertools
import pickle

download('stopwords', quiet=True)
download('omw',quiet=True)
stop_words = set(stopwords.words('english'))
synsets = dict(pickle.load(pkg_resources.resource_stream(__name__,"data/command_synsets.veronica")))
config_dictionary={}
for pos,offset in synsets:
    config_dictionary[wordnet.synset_from_pos_and_offset(pos,offset)]=synsets[(pos,offset)]
print(config_dictionary)

class Veronica(Friendly,Information):

    def precmd(self, line):
        line = line.lower()
        search_query= word_tokenize(line);
        processed_search_query=[]
        for token in search_query:
            if(token not in stop_words):
                processed_search_query.append(token)
        logging.debug("Preprocessed query: {}".format(" ".join(processed_search_query)))
        
        allcmds=[i[3:] for i in dir(self) if ismethod(getattr(self,i)) and i[:3]=="do_"]
        logging.debug("Available command tags: {}".format(str(allcmds)))

        # If query exactly matches the command key
        # if(processed_search_query[0] in allcmds):
        #     return " ".join(processed_search_query)
        # usercmd= wordnet.synsets(processed_search_query[0])
        
        
        # with open("dict_to_json_textfile.json", 'w') as fout:
        #     json_dumps_str = json.dumps(allcmds_dict, indent=4)
        #     print(json_dumps_str, file=fout)
        # similarity={}
        # for w1 in usercmd:
        #     for w2 in allcmds_synsets:
        #         sim=wordnet.path_similarity(w1,w2)
        #         if(sim==None): sim=0
        #         similarity[(w1.name().partition('.')[0],w2.name().partition('.')[0])]=sim
        # similarity_list=sorted(similarity, key=similarity.__getitem__, reverse=True)
        # logging.debug("Synset similarity: {}".format(str(similarity_list)))
        # if(similarity[similarity_list]>)

        # if(usercmd):
        #     for allcmd in allcmds:
        #         allcmd_synsets= wordnet.synsets(allcmd)
        #         print(allcmd_synsets)
        #         if(allcmd_synsets):
        #             print(processed_search_query[0],allcmd,usercmd[0].wup_similarity(allcmd_synsets[0]))
        
        
        

        # Get all relevant function names from this next line.
        # [i for i in dir(self) if ismethod(getattr(self,i)) and i[:3]=="do_"]
        

    def postloop(self):
        print("Thank you!")

def argParse(argx):
    logging.debug(argx)

def main():
    """Console script for veronica."""
    # sentry_sdk.init("https://3ac0bcf6b7c94dceba16841163e807d0@o410546.ingest.sentry.io/5299322")
    logging.basicConfig(level=logging.DEBUG)
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
