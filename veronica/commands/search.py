

from googleapiclient.discovery import build
import argparse
from veronica.unit import unit
from pathlib import Path
from rich.table import Table

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
    fileglob= args[0]
    pathglob="."
    if(len(args)>1):
        pathglob= args[1]

    table = Table()
    table.add_column("Recieved At")
    table.add_column("From")
    table.add_column("Subject")
    table.add_column("Labels")
    relevant_files= list(str(i).split(".") for i in Path(pathglob).glob(fileglob))
    
    creds = self.vx_google_setup()

    


    # # do something with "txt_file"

    # service = build('drive', 'v3', credentials=creds)
    # results = service.files().list().execute()
    # print(results["files"])
