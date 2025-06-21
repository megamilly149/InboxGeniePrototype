# tests/test_text_prediction.py
import unittest
from services.Text_Prediction_Service import generate_email_response

class TestTextPrediction(unittest.TestCase):
    
    def test_generate_email_response(self):
        response = generate_email_response("Meeting Request", "example@domain.com", "Hi, I would like to schedule a meeting.")
        self.assertTrue(response.startswith("Dear"))
    
if __name__ == "__main__":
    unittest.main()
