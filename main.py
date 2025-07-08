# main.py

import pinecone
import openai
from appconfig import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, PINECONE_API_KEY, PINECONE_ENVIRONMENT

# Azure OpenAI setup
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_OPENAI_ENDPOINT  # Setting the endpoint for Azure OpenAI

# Pinecone setup
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
index = pinecone.Index("your_index_name")  # Replace with your actual index name

# Example of using both Azure OpenAI and Pinecone
def generate_email_response(subject, sender, previous_conversation=""):
    """
    Generate a professional email response based on the subject, sender, and previous conversation.
    
    Args:
        subject (str): The subject of the email.
        sender (str): The sender's email address.
        previous_conversation (str, optional): The prior email conversation or context. Defaults to an empty string.
    
    Returns:
        str: The generated email response.
    """
    
    # Construct the prompt for the model
    prompt = (
        f"Write a professional email response to the following email from {sender}. "
        f"Subject: {subject}. Previous conversation: {previous_conversation}"
    )
    
    try:
        # Request the model to generate a response using Azure OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or gpt-4 if available
            prompt=prompt,
            max_tokens=150
        )
        
        # Return the generated response text
        return response.choices[0].text.strip()

    except openai.error.OpenAIError as e:
        # Handle any API errors (e.g., network issues or invalid credentials)
        print(f"Error generating response: {e}")
        return "Sorry, we encountered an error while generating the response."

# Example usage
subject = "Meeting Request"
sender = "example@domain.com"
previous_conversation = "Hi, I would like to schedule a meeting."

response = generate_email_response(subject, sender, previous_conversation)
print(f"Suggested Response: {response}")

    