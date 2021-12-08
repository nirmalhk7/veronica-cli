from getpass import getuser
from rich.progress import Progress
from googleapiclient.discovery import build

class UserInterface():
    firstname       = None
    middlename      = None
    lastname        = None
    phone_numbers   = None
    email           = None
    birthdate       = None
    gender          = None
    streetAddress   = None
    city            = None
    postalCode      = None
    countryCode     = None
    picture         = None
    system_username = getuser()
    def get_name(self):
        return self.firstname or self.system_username.capitalize()
    def sanitise(self,statement):
        return statement
    
    def load(self):
        creds = self.vx_google_setup()
        service1 = build('oauth2', 'v2', credentials=creds)
        service2 = build('people', 'v1', credentials=creds)
        with Progress(transient=True) as progress:
            t1= progress.add_task("[red]Loading ...",start=False)
            results1 = service1.userinfo().get().execute()
            results2 = service2.people().get(resourceName="people/me",personFields="addresses,ageRanges,biographies,birthdays,calendarUrls,clientData,coverPhotos,emailAddresses,events,externalIds,genders,imClients,interests,locales,locations,memberships,metadata,miscKeywords,names,nicknames,occupations,organizations,phoneNumbers,photos,relations,sipAddresses,skills,urls,userDefined",
            ).execute()