# Test the FIRST available model
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

print("Finding first working model...\n")

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        model_name = m.name
        print(f"Testing: {model_name}")
        
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Hello Miku!' in one line")
            print(f"\n🎯 SUCCESS! Working Model: {model_name}")
            print(f"Response: {response.text}\n")
            print(f"✅ USE THIS IN CONFIG: {model_name}\n")
            break
        except Exception as e:
            print(f"Failed: {str(e)[:80]}\n")
