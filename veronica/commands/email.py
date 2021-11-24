from veronica.voice import vx_print
from googleapiclient.discovery import build


def do_email(self, args):
    """
        Print upcoming latest important and unread emails
    """
    try:
        creds = self.vx_google_setup(self)
    except TypeError:
        creds = self.vx_google_setup()
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(
        userId='me',
        includeSpamTrash=False,
        maxResults=20,
        labelIds=["INBOX", "IMPORTANT",
                  "UNREAD"]).execute().get('messages', [])
    
    print(results)
    # for i in results:
    #     mail= service.users().messages().get(
    #         userId='me',
    #         id=i["id"]
    #     ).execute().get("payload",[])
    #     print(i["id"], mail)