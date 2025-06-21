import requests
import msal
from services.EmailModel import EmailModel

class EmailParserService:
    def __init__(self):
        self.client_id = "your_client_id_here"
        self.client_secret = "your_client_secret_here"
        self.tenant_id = "your_tenant_id_here"
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"

    def get_emails(self):
       
        token = self._authenticate()
        emails = self._fetch_emails(token)
        email_objects = [EmailModel(email["subject"], email["from"]["emailAddress"]["address"], email["body"]["content"], email.get("attachments", [])) for email in emails]
        return email_objects

    def _authenticate(self):
        app = msal.ConfidentialClientApplication(self.client_id, authority=self.authority, client_credential=self.client_secret)
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception("Failed to obtain access token")

    def _fetch_emails(self, token):
        url = "https://graph.microsoft.com/v1.0/me/messages"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                return response.json().get("value", [])
            except ValueError:
                raise Exception("Failed to decode JSON response")
        else:
            raise Exception(f"Failed to fetch emails: {response.status_code} {response.text}")

    def parse_attachments(self, email):
      
        attachments = email.attachments
       
        return attachments

