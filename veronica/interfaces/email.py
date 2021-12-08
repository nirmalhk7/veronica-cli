class EmailsInterface():
    starred = None
    category_color = None
    Date = None
    From = None
    Subject = None
    labels = None

    def __init__(self, mail_id) -> None:
        self.id = mail_id

    def get(self):
        link = "https://mail.google.com/mail/u/0/#inbox/"

        return ("[{} {}]{}[/]".format(self.starred, self.category_color, self.Date),
                "[{} {}]{}[/]".format(self.starred, self.category_color, self.From),
                "[{} {}][link={}]{}[/link][/]".format(
            self.starred, self.category_color, self.category_color, link+self.id, self.Subject),
            "[{} {}]{}[/]".format(self.starred, self.category_color, self.labels))
