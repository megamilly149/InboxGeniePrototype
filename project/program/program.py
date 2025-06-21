import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import openai
from ..appconfig.AppConfig import OPENAI_API_KEY


openai.api_key = OPENAI_API_KEY

try:
   
    response = openai.completions.create(
        model="gpt-3.5-turbo",  
        prompt="Write a poem about AI",  
        max_tokens=100
    )
    
   
    generated_text = response['choices'][0]['text'].strip()
    print(generated_text)

except openai.error.OpenAIError as e:
    print(f"OpenAI error occurred: {e}")

except Exception as e:
    print(f"An error occurred: {e}")
