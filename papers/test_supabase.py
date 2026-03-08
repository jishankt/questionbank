import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = f"{os.getenv('SUPABASE_URL')}/storage/v1/object/{os.getenv('SUPABASE_BUCKET')}/test.txt"
headers = {
    "Authorization": f"Bearer {os.getenv('SUPABASE_KEY')}",
    "Content-Type": "text/plain",
    "x-upsert": "true"
}

response = requests.post(url, headers=headers, data=b"hello supabase")
print("Status:", response.status_code)
print("Response:", response.text)