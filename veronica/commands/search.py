

from googleapiclient.discovery import build

from veronica.unit import unit


@unit(label="Find a file")
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
