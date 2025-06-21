
import openai
from AppConfig import OPENAI_API_KEY  # API key from AppConfig

openai.api_key = OPENAI_API_KEY

def generate_email_response(subject, sender, previous_conversation=""):
    """Generate email response suggestion based on subject and sender"""

    # Create a prompt for generating a response
    prompt = f"Write a professional email response to the following email from {sender}. Subject: {subject}. Previous conversation: {previous_conversation}"
    
    # Request the model to generate a response
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # Or gpt-4 if available
        prompt=prompt,
        max_tokens=150
    )

    return response.choices[0].text.strip()

# Example Usage
subject = "Meeting Request"
sender = "example@domain.com"
previous_conversation = "Hi, I would like to schedule a meeting."
response = generate_email_response(subject, sender, previous_conversation)
print(f"Suggested Response: {response}")
