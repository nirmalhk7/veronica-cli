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
from nltk.corpus import stopwords, wordnet as wn
from inspect import ismethod
import logging
import json
import itertools
import pickle

logging.basicConfig(level=logging.INFO)
download('stopwords', quiet=True)
download('omw',quiet=True)
stop_words = set(stopwords.words('english'))
synsets = dict(pickle.load(pkg_resources.resource_stream(__name__,"data/command_synsets.veronica")))
config_dictionary={}
for pos,offset in synsets:
    config_dictionary[wn.synset_from_pos_and_offset(pos,offset)]=synsets[(pos,offset)]
logging.debug("Command config: {}".format(str(config_dictionary)))


class Veronica(Friendly,Information):
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

        usercmd_sysnets= wn.synsets(processed_search_query[0])
        similarity={}
        for net in usercmd_sysnets:
            for v_cmd in config_dictionary.keys():
                similarity[(v_cmd,net)]=v_cmd.wup_similarity(net) or 0
        similarity_list=sorted(similarity, key=similarity.__getitem__, reverse=True)
        
        if(similarity_list and similarity[similarity_list[0]]>0.85):
            max_similarity_key=similarity_list[0]
            command=config_dictionary[max_similarity_key[0]]
            logging.debug("Sorted similarity: {}".format(similarity_list))
            logging.info("Max similarity: {} at {}".format(str(max_similarity_key),similarity[similarity_list[0]]))
            logging.debug("Reprocessed command: {}".format(command))
            getattr(self,"do_"+command)(1)
            return ""
        else: 
            return " ".join(processed_search_query)


        

    def postloop(self):
        print("Thank you!")

def argParse(argx):
    logging.debug(argx)


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
