import unittest
from unittest.mock import patch, MagicMock
from services.EmailParserService import EmailParserService
from services.EmailModel import EmailModel

class TestEmailParser(unittest.TestCase):
    
    @patch.object(EmailParserService, '_fetch_emails')  # Mock the _fetch_emails method
    def test_get_emails(self, mock_fetch_emails):
        # Sample mock email data to return
        mock_email_data = [
            {
                "subject": "Meeting Reminder",
                "from": {"emailAddress": {"address": "sender@example.com"}},
                "body": {"content": "This is a reminder for our meeting tomorrow."},
                "attachments": []
            },
            {
                "subject": "Invoice",
                "from": {"emailAddress": {"address": "billing@example.com"}},
                "body": {"content": "Please find the invoice attached."},
                "attachments": []
            }
        ]
        
        # Set the mock method to return our sample email data
        mock_fetch_emails.return_value = mock_email_data
        
        # Instantiate EmailParserService and call get_emails
        service = EmailParserService()
        email_objects = service.get_emails()
        
        # Assertions
        self.assertEqual(len(email_objects), 2)  # We should have 2 mock emails
        self.assertIsInstance(email_objects[0], EmailModel)  # Check that EmailModel objects are returned
        self.assertEqual(email_objects[0].subject, "Meeting Reminder")
        self.assertEqual(email_objects[0].sender, "sender@example.com")
        
    @patch.object(EmailParserService, '_fetch_emails')
    def test_get_emails_empty(self, mock_fetch_emails):
        # Mock an empty email list
        mock_fetch_emails.return_value = []
        
        service = EmailParserService()
        email_objects = service.get_emails()
        
        # Assertions
        self.assertEqual(len(email_objects), 0)  # No emails should be returned
    
if __name__ == "__main__":
    unittest.main()

