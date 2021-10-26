import geocoder
import requests
from pip._vendor.colorama import Fore

from veronica.voice import vx_print


def do_weather(self,args):
    def f_to_c(x):
        return str(round((x - 32) * 5.0/9.0,2))

    locError = False

    vx_print("Retreiving weather for "+(args.capitalize() if args else "your current location")+" ... ", speak=False)
    if (args != ""):
        coord = g.latlng
    elif (args == "" or locError):
        g = geocoder.ip('me')
        coord = g.latlng
    if(self.env["WEATHER_DARKSKY"]):
        response = requests.get('https://api.darksky.net/forecast/'+self.env["WEATHER_DARKSKY"]+'/'+str(coord[0])+','+str(coord[1]))
        if(response.status_code == 200):
            data = response.json()
            res = data['currently']['summary']+" today with "+f_to_c(data['currently']['temperature'])+"° C."
            if(data['currently']['precipProbability']>0.5):
                res += " Expect a "+str(data['currently']['precipProbability']*100)+"% chance of "+data['currently']['precipType']+"."
            vx_print("")
            vx_print(res,color=Fore.GREEN)
            vx_print("")
        else:
            vx_print("Error: "+response.status_code)
