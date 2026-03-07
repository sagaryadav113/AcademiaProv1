import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("ERROR: GOOGLE_API_KEY not found in .env file")
    exit(1)

genai.configure(api_key=api_key)

print("--- FETCHING ALLOWED MODELS ---")
try:
    # This will list every model and its raw data
    for model in genai.list_models():
        print(f"MODEL ID: {model.name}")
except Exception as e:
    print(f"Error: {e}")
