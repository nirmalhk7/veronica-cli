import pickle
from collections import defaultdict
class Company(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

a=defaultdict()
a[Company('1','1')]=[2,3,4,5]
with open('command_synsts.dictionary','wb') as f:
    pickle.dump(a,f,pickle.HIGHEST_PROTOCOL) 