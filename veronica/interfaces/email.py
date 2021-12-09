class EmailsInterface():
    starred = ""
    category_color = None
    Date = None
    From = None
    Subject = None
    labels = None
    
    
    def __init__(self, mail_id) -> None:
        self.id = mail_id


