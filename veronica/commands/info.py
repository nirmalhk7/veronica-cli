import geocoder
import requests

from rich import print



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
        if(response.status_code == 200):
            data = response.json()
            for i in range(limit):
                try:
                    res = data['itemListElement'][i]['result']
                    print("")
                    try:
                        print(res['name'])
                    except KeyError:
                        pass
                    try:
                        print(res['description'])
                    except KeyError:
                        pass
                    try:    
                        print(res['detailedDescription']['articleBody'])
                    except KeyError:
                        pass
                    try:    
                        print(res['detailedDescription']['url'])
                    except KeyError:
                        pass
                    print("")
                except IndexError:
                    print("Sorry, no data available!")
        else:
            print("Error: {}".format(str(response)),speakText="Sorry, there's been some kind of an error.")
