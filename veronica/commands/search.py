from veronica.config import component
from veronica.voice import vx_print

@component
def do_search(self,args):
    """
        Search file at location, or search at Google.
        Example:
            veronica search ~/Documents --ext txt       ===> Lists all txt files in Documents folder (recursively)
            veronica search Red Bull Racing             ===> Queries at Google
    """
    args= args.split(" ")
    # for parent_path, _, filenames in os.walk(Path.home()):
    # for f in filenames:
    #     print(os.path.join(parent_path, f))

    vx_print("Search: WIP",speak=False)

    pass