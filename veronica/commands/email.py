from googleapiclient.discovery import build
from veronica.config import component
from veronica.voice import vx_print

@component
def do_email(self,args):
    """
        Print upcoming latest important and unread emails
    """
    try:
        creds = self.vx_google_setup(self,self.SCOPES)
    except TypeError:
        creds = self.vx_google_setup(self.SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    results=  service.users().messages().list(userId='me').execute().get('messages')
    print(results)
    pass