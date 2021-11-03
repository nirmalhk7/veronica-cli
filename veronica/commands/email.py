from veronica.voice import vx_print
from googleapiclient.discovery import build
import base64

def do_email(self, args):
    """
        Print upcoming latest important and unread emails
    """
    try:
        creds = self.vx_google_setup(self, self.SCOPES)
    except TypeError:
        creds = self.vx_google_setup(self.SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(
        userId='me',
        includeSpamTrash=False,
        maxResults=20,
        labelIds=["INBOX", "IMPORTANT",
                  "UNREAD"]).execute().get('messages', [])
    
    print(service.users().messages().list(
        userId='me',
        includeSpamTrash=False,
        maxResults=20,
        labelIds=["INBOX", "IMPORTANT",
                  "UNREAD"]).execute())
    allmail=[]
    for i in results:
        mailinfo= service.users().messages().get(
            userId='me',
            id=i["id"]
        ).execute().get("payload",{}).get("headers",[])
        mailinfo=[i for i in mailinfo if i["name"] in ["Subject","From","Date"]]
        
        mailinfo_hx={}
        for i in mailinfo:
            mailinfo_hx[i["name"]]=i["value"]
        mailinfo_hx["id"]=i["id"]
        allmail.append(mailinfo_hx)
    print(allmail)
        
    pass