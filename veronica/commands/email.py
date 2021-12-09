from rich.progress import Progress

from rich.table import Table
from googleapiclient.discovery import build
import json
from datetime import date, datetime

from veronica.unit import unit

from veronica.interfaces.email import EmailsInterface

style_hash = {
    "CATEGORY_FORUMS": "#FFA701",
    "CATEGORY_UPDATES": "#FFBA01",
    "CATEGORY_PERSONAL": "FFFF33",
    "CATEGORY_PROMOTIONS": "#FFE800",
    "CATEGORY_SOCIAL": "#FFDA00"
}


@unit(label=["Check mails", "Any new emails?", "Check my mails"])
def do_email(self, args):
    """
        Print upcoming latest important and unread emails
    """
    creds = self.vx_google_setup()
    service = build('gmail', 'v1', credentials=creds)
    with Progress(transient=True) as progress:
        t1 = progress.add_task("[red]Loading emails ...", start=False)
        results = service.users().messages().list(
            userId='me',
            includeSpamTrash=False,
            maxResults=20,
            labelIds=["INBOX", "IMPORTANT",
                      "UNREAD"]).execute().get('messages', [])

        table = Table()
        table.add_column("Recieved At")
        table.add_column("From")
        table.add_column("Subject")
        table.add_column("Labels")

        mails = []
        for i in results:
            mail = service.users().messages().get(
                userId='me',
                id=i["id"]
            ).execute()

            mailobj = EmailsInterface(mail["id"])

            for i in mail["labelIds"]:
                if(i in style_hash.keys()):
                    mailobj.category_color = style_hash[i]
                if(i == "STARRED"):
                    mailobj.starred = "bold "
                if(i[:6] == "Label_"):
                    mailobj.labels = " ".join(service.users().labels().get(
                        userId="me", id=i).execute().get("name"))

            for item in mail["payload"].get("headers", []):
                if(item["name"] in ["From", "Subject", "Date"]):
                    setattr(mailobj, item["name"], item["value"])

            mails.append(mailobj)

        link = "https://mail.google.com/mail/u/0/#inbox/"
        for i in mails:
            table.add_row(
                "[{}{}]{}[/]".format(i.starred,i.category_color ,i.Date),
                "[{}{}]{}[/]".format(i.starred,i.category_color ,i.From),
                "[{}{}][link={}]{}[/link][/]".format(i.starred,i.category_color,link+i.id,i.Subject),
                "[{}{}]{}[/]".format(i.starred,i.category_color ,i.labels),   
            )

    self.output.print(
        table, speakMsg="You have {} new emails".format(len(mails)))
