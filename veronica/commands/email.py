from veronica.voice import vx_print
from googleapiclient.discovery import build
from datetime import datetime, timezone

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
    
    allmail=[]
    for i in results:
        mailinfo= service.users().messages().get(
            userId='me',
            id=i["id"]
        ).execute().get("payload",{}).get("headers",[])
        mailinfo=[i for i in mailinfo if i["name"] in ["Subject","From","Date"]]
        
        mailinfo_hx={}
        for j in mailinfo:
            mailinfo_hx[j["name"]]=j["value"]

        mailinfo_hx["id"]=i["id"]
        if "Date" in mailinfo_hx:
            mailinfo_hx["Date"]= datetime.strptime(mailinfo_hx["Date"],"%a, %d %b %Y %H:%M:%S %z (%Z)").replace(tzinfo=timezone.utc).astimezone(tz=None)
        allmail.append(mailinfo_hx)
    print(allmail)
        
    pass