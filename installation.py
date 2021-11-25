from veronica.cli import Veronica
import pickle
from pathlib import Path
from nltk.corpus import wordnet as wn
from veronica.cli import Veronica

method_names = [attr[3:] for attr in dir(Veronica) if attr[:3] == "do_"]
synsets_all = {}

for method in method_names:
    method_synsets = wn.synsets(method)
    for synset in method_synsets:
        synsets_all[(synset.name().split('.')[1],
                        synset.offset())] = method

with open("veronica/data/module.weights", 'wb') as cn:
    pickle.dump(synsets_all, cn)
