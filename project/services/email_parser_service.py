import requests
import msal
import openai
from services.EmailModel import EmailModel
import pinecone
import appconfig
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

class EmailParserService:
    def __init__(self):
        # Azure credentials
        self.client_id = "your_client_id_here"
        self.client_secret = "your_client_secret_here"
        self.tenant_id = "your_tenant_id_here"
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.openai_api_key = appconfig.OPENAI_API_KEY
        self.pinecone_api_key = appconfig.PINECONE_API_KEY
        self.pinecone_environment = appconfig.PINECONE_ENVIRONMENT
        
        # Set up Azure Text Analytics Client
        self.text_analytics_client = self._get_text_analytics_client()

        # Initialize Pinecone
        pinecone.init(api_key=self.pinecone_api_key, environment=self.pinecone_environment)
        self.index = pinecone.Index("inbox-genie-index")  # Example index

    def get_emails(self):
        """Authenticate and fetch emails, returning them as EmailModel objects."""
        try:
            # Authenticate and get the access token
            token = self._authenticate()
            
            # Fetch emails using the obtained token
            emails = self._fetch_emails(token)
            
            # Convert raw email data into EmailModel instances
            email_objects = [EmailModel(email["subject"], email["from"]["emailAddress"]["address"],
                                        email["body"]["content"], email.get("attachments", [])) 
                             for email in emails]
            return email_objects
        except Exception as e:
            # Handle errors during email fetching and parsing
            print(f"Error while getting emails: {e}")
            return []

    def _authenticate(self):
        """Authenticate using client credentials and return the access token."""
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        
        # Attempt to acquire an access token
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

        # Check if the token was successfully acquired
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception("Failed to obtain access token")

    def _fetch_emails(self, token):
        """Fetch the emails from the Microsoft Graph API using the access token."""
        url = "https://graph.microsoft.com/v1.0/me/messages"
        headers = {"Authorization": f"Bearer {token}"}

        # Send request to fetch emails
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            try:
                # Parse the JSON response and return the email data
                return response.json().get("value", [])
            except ValueError:
                raise Exception("Failed to decode JSON response")
        else:
            raise Exception(f"Failed to fetch emails: {response.status_code} {response.text}")

    def _get_text_analytics_client(self):
        """Setup and return the Text Analytics client for Azure."""
        credential = AzureKeyCredential(appconfig.AZURE_SPEECH_KEY)
        return TextAnalyticsClient(endpoint="https://<YOUR_REGION>.api.cognitive.microsoft.com/", credential=credential)

    def _generate_embeddings(self, email_content):
        """Generate embeddings using OpenAI API (via Azure OpenAI)."""
        openai.api_key = self.openai_api_key
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=email_content
        )
        return response['data'][0]['embedding']

    def _search_similar_emails(self, email_content):
        """Use Pinecone to search for the most similar emails."""
        query_embedding = self._generate_embeddings(email_content)
        result = self.index.query(query_embedding, top_k=3)
        return result['matches']

    def _generate_email_response(self, relevant_emails, user_query):
        """Generate email response using Azure OpenAI, with RAG."""
        context = " ".join([email['id'] for email in relevant_emails])
        prompt = f"Generate a professional email response considering the following context: {context} \nQuery: {user_query}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def parse_attachments(self, email):
        """Parse and return the attachments of an email."""
        try:
            attachments = email.attachments
            return attachments
        except AttributeError:
            return []

    def handle_incoming_email(self, incoming_email):
        """Process incoming email and generate a response using RAG."""
        # First, get similar emails from Pinecone
        relevant_emails = self._search_similar_emails(incoming_email['body']['content'])
        
        # Generate an email response using Azure OpenAI
        user_query = "Generate a response to this email"
        email_response = self._generate_email_response(relevant_emails, user_query)
        
        return email_response
