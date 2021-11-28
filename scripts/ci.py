from veronica.cli import Veronica
import pickle
from pathlib import Path
from veronica.cli import Veronica
from json import dump

nlp= pickle.load(open("veronica/data/en_core_web_md","rb"))

def prebuild():
    unit_hash={}
    method_names = [attr for attr in dir(Veronica) if attr[:3] == "do_" and attr!="do_EOF"]
    for method in method_names:
        if('nlp' in dir(getattr(Veronica,method))):
            for label in getattr(Veronica,method).nlp:
                unit_hash[nlp(label)]=method[3:]
    
    print(unit_hash)
    with open("veronica/data/module.weights.json", 'wb') as cn:
        pickle.dump(unit_hash, cn)

prebuild()