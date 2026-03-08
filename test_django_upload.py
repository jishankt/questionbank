import django
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "questionbank.settings")
django.setup()

from django.core.files.base import ContentFile
from papers.supabase_storage import SupabaseStorage

storage = SupabaseStorage()

# Test upload
print("Uploading test PDF...")
name = storage._save("question_papers/test_upload.pdf", ContentFile(b"%PDF-1.4 test content"))
print(f"Saved as: {name}")

# Test URL
url = storage.url(name)
print(f"Public URL: {url}")

# Test exists
print(f"Exists: {storage.exists(name)}")