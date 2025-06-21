class EmailModel:
    def __init__(self, subject, sender, body, attachments):
        self.subject = subject
        self.sender = sender
        self.body = body
        self.attachments = attachments