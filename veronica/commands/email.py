from veronica.voice import vx_print
from googleapiclient.discovery import build
from datetime import datetime, timezone
from rich.table import Table

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
    table= Table()
    table.add_column("From")
    table.add_column("Subject")
    table.add_column("Date")
    
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
            mailinfo_hx["Date"]= datetime.strptime(mailinfo_hx["Date"],"%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=timezone.utc).astimezone(tz=None)
        allmail.append(mailinfo_hx)
        rootlink="https://mail.google.com/mail/u/0/#inbox/"+mailinfo_hx["id"]
        table.add_row(
            "[link={}]{}[/link]".format(rootlink,mailinfo_hx["From"]),
            "[link={}]{}[/link]".format(rootlink,mailinfo_hx["Subject"]),
            "[link={}]{}[/link]".format(rootlink,str(mailinfo_hx["Date"]))
        )

    self.console.print(table)

    pass