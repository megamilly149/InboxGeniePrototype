import unittest
from services.Text_Prediction_Service import generate_email_response

class TestTextPrediction(unittest.TestCase):
    
    def test_generate_email_response(self):
        subject = "Meeting Request"
        sender = "example@domain.com"
        message = "Hi, I would like to schedule a meeting."
        
        # Call the real function
        response = generate_email_response(subject, sender, message)
        
        self.assertTrue(response.startswith("Dear"))
        self.assertIn(sender, response)
        self.assertIn("schedule a meeting", response)

    def test_generate_email_response_empty(self):
        subject = "Meeting Request"
        sender = "example@domain.com"
        message = ""

        response = generate_email_response(subject, sender, message)
        
        self.assertEqual(response, "")

if __name__ == "__main__":
    unittest.main()


