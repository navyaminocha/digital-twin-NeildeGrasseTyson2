from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv()


client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def ask_gemini(prompt):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemma-4-31b-it",
                contents=prompt
            )
            return response.text
        
    

        except Exception as e:

            print(f"Attempt {attempt+1} failed:", e)

            if attempt < 2:
                time.sleep(5)
            else:
                raise e