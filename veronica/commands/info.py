import webbrowser
import requests

from rich import print

from veronica.unit import unit


@unit(label=["What are laws of thermodynamics?","What is earth?","Who is Elon Musk?","Where is Cambodia?","Tell me about London"])
def do_info(self,args):
    print("Retreiving information for your query ... ")
    try:
        query,limit = args.split(':')
        limit = int(limit)
    except ValueError:
        query = args
        limit = 1
    
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    if(self.settings["env"]["KNOWLEDGE_GRAPH"]):
        parameters = {
            'query': query,
            'limit': limit,
            'indent': True,
            'key': self.settings["env"]["KNOWLEDGE_GRAPH"],
        }
        response = requests.get(service_url,params=parameters)
        anyError=False
        if(response.status_code == 200):
            data = response.json()
            for i in range(limit):
                try:
                    res = data['itemListElement'][i]['result']
                    print("")
                    try:
                        print(res['name'])
                    except KeyError:
                        anyError=True
                    try:
                        print(res['description'])
                    except KeyError:
                        anyError=True
                    try:    
                        print(res['detailedDescription']['articleBody'])
                    except KeyError:
                        anyError=True
                    try:    
                        print(res['detailedDescription']['url'])
                    except KeyError:
                        anyError=True
                    print("")
                except IndexError:
                    anyError=True
        else:
            print("Error: {}".format(str(response)),speakText="Sorry, there's been some kind of an error.")
            webbrowser.open("https://www.google.com/search?q={}".format(query))
