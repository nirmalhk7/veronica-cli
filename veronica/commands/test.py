from rich.progress import Progress

from rich.table import Table
from googleapiclient.discovery import build
import json
from datetime import date, datetime

# https://googleapis.github.io/google-api-python-client/docs/dyn/oauth2_v2.userinfo.html#get


def do_test(self, args):
    """
        Print upcoming latest important and unread emails
    """
    
    creds = self.vx_google_setup()
    service1 = build('oauth2', 'v2', credentials=creds)
    service2 = build('people', 'v1', credentials=creds)
    with Progress(transient=True) as progress:
        t1= progress.add_task("[red]Loading ...",start=False)
        results1 = service1.userinfo().get().execute()
        results2 = service2.people().get(resourceName="people/me",personFields="addresses,ageRanges,biographies,birthdays,calendarUrls,clientData,coverPhotos,emailAddresses,events,externalIds,genders,imClients,interests,locales,locations,memberships,metadata,miscKeywords,names,nicknames,occupations,organizations,phoneNumbers,photos,relations,sipAddresses,skills,urls,userDefined",
        ).execute()
        print(results1)
        print(results2)