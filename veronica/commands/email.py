from veronica.voice import vx_print
from googleapiclient.discovery import build


def email(self, args):
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
    
    for i in results:
        mail= service.users().messages().get(
            userId='me',
            id=i["id"]
        ).execute().get("payload",[])
        print(i["id"], mail)
    pass