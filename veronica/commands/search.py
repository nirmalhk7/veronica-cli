from veronica.config import unit
from veronica.voice import vx_print
from googleapiclient.discovery import build


@unit
def search(self, args):
    """
        Search file at location, or search at Google.
        Example:
            veronica search partialFilename ~/Documents:
                Lists all files with name containing partialFilename  
                locally as well as on Google Drive 
                if file is not available anywhere
    """
    args = args.split(" ")

    try:
        creds = self.vx_google_setup(self, self.SCOPES)
    except TypeError:
        creds = self.vx_google_setup(self.SCOPES)

    service = build('drive', 'v3', credentials=creds)
    results = service.files().list().execute()
    print(results["files"])
