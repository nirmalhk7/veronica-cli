
from logging import root
from random import randint
import pkg_resources
import json
from veronica.veronica import root_path
from veronica.voice import vx_print

def do_joke(self,args):
    data= json.loads(pkg_resources.resource_string(root_path(),"/data/jokes.json").decode("utf-8","ignore"))
    vx_print(data[randint(0,len(data)-1)])