from veronica.config import component
from veronica.voice import vx_print

@component
def do_email(self,args):
    """
        Print upcoming latest important and unread emails
    """
    vx_print("Email: WIP",speak=False)
    pass