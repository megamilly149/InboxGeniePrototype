# tests/test_email_parser.py

import unittest
from services.EmailParserService import get_emails

class TestEmailParser(unittest.TestCase):
    
    def test_get_emails(self):
        subject, sender = get_emails("your-email@gmail.com", "your-email-password")
        self.assertIsNotNone(subject)
        self.assertIsNotNone(sender)
    
if __name__ == "__main__":
    unittest.main()
