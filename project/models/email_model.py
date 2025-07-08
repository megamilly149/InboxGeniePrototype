class EmailModel:
    def __init__(self, subject: str, sender: str, body: str, attachments: list = None):
        """
        Initializes the EmailModel instance with the provided email details.

        Args:
            subject (str): The subject of the email.
            sender (str): The sender's email address.
            body (str): The body/content of the email.
            attachments (list, optional): A list of attachments (default is None).

        Attributes:
            subject (str): The subject of the email.
            sender (str): The sender's email address.
            body (str): The body/content of the email.
            attachments (list): A list of email attachments. If none, defaults to an empty list.
        """
        self.subject = subject
        self.sender = sender
        self.body = body
        self.attachments = attachments if attachments else []  # Defaults to empty list if None is provided

    def __str__(self):
        """Return a string representation of the EmailModel instance."""
        return f"Subject: {self.subject}\nFrom: {self.sender}\nBody: {self.body[:50]}..."  # Limiting body to 50 chars for preview

    def add_attachment(self, attachment):
        """Add an attachment to the email."""
        if attachment not in self.attachments:
            self.attachments.append(attachment)

    def remove_attachment(self, attachment):
        """Remove an attachment from the email."""
        if attachment in self.attachments:
            self.attachments.remove(attachment)

    def get_attachments(self):
        """Return the list of attachments."""
        return self.attachments

    def is_empty(self):
        """Check if the email content (subject, sender, body) is empty."""
        return not self.subject and not self.sender and not self.body
