import geocoder
import requests
from rich.progress import Progress
from veronica.unit import unit

@unit(label="Current weather in a city")
def do_weather(self,args):
    def f_to_c(x):
        return str(round((x - 32) * 5.0/9.0,2))

    with Progress(transient=True) as progress: 
        t1= progress.add_task("[blue]Retrieving coordinates for {} ...".format(args.capitalize() if args else "your current location"),start=False)
        if (args != ""):
            g = geocoder.osm(args)
        elif (args == ""):
            g = geocoder.ip('me')
        coord = g.latlng
        t2= progress.add_task("[violet]Fetching weather conditions ...")
        if(self.settings["env"]["WEATHER_DARKSKY"]):
            response = requests.get('https://api.darksky.net/forecast/'+self.settings["env"]["WEATHER_DARKSKY"]+'/'+str(coord[0])+','+str(coord[1]))
    if(response and response.status_code == 200):
        data = response.json()
        res = data['currently']['summary']+" today with "+f_to_c(data['currently']['temperature'])+"° C."
        if(data['currently']['precipProbability']>0.5):
            res += " Expect a "+str(data['currently']['precipProbability']*100)+"% chance of "+data['currently']['precipType']+"."
        print("")
        print(res)
        print("")
    else:
        print("Error: "+response.status_code)
