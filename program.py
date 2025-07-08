import sys
import os

# Add the root directory to the sys.path so that you can import appconfig
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import openai
from appconfig.appconfig import OPENAI_API_KEY  # Import API key from appconfig.py

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

try:
    # Make the request to OpenAI for text generation
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # You can use "gpt-4" if available
        prompt="Write a poem about AI",  # Example prompt
        max_tokens=100
    )
    
    # Process and print the generated response
    generated_text = response['choices'][0]['text'].strip()
    print(generated_text)

except openai.error.OpenAIError as e:
    print(f"OpenAI error occurred: {e}")

except Exception as e:
    print(f"An error occurred: {e}")
