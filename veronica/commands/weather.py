import geocoder
import requests
from pip._vendor.colorama import Fore


def do_weather(self,args):
    locError = False
    
    if (args != ""):
        print("Retreiving weather for "+args.capitalize()+" ... ")
        g = geocoder.arcgis(args)
        print(g)
        coord = g.latlng
    elif (args == "" or locError):
        print("Retrieving weather for your current location ... ")
        g = geocoder.ip('me')
        coord = g.latlng
    if(self.env["WEATHER_DARKSKY"]):
        response = requests.get('https://api.darksky.net/forecast/'+self.env["WEATHER_DARKSKY"]+'/'+str(coord[0])+','+str(coord[1]))
        if(response.status_code == 200):
            data = response.json()
            res = data['currently']['summary']+" today with "+f_to_c(data['currently']['temperature'])+"° C."
            if(data['currently']['precipProbability']>0.5):
                res += " Expect a "+str(data['currently']['precipProbability']*100)+"% chance of "+data['currently']['precipType']+"."
            print("")
            print(Fore.GREEN+res)
            print("")
        else:
            print("Error: "+response.status_code)
