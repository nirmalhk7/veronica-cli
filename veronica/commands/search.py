from veronica.config import unit
from veronica.voice import vx_print
from googleapiclient.discovery import build



def do_search(self, args):
    """
        Search file at location, or search in Google Drive.
        Example:
            veronica search partialFilename ~/Documents:
                Lists all files with name containing partialFilename  
                locally as well as on Google Drive 
                if file is not available anywhere
    """
    args = args.split(" ")

    try:
        creds = self.vx_google_setup(self)
    except TypeError:
        creds = self.vx_google_setup()

    service = build('drive', 'v3', credentials=creds)
    results = service.files().list().execute()
    print(results["files"])
