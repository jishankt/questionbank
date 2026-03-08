import os, sys, django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "questionbank.settings")
django.setup()

import requests
from django.conf import settings
from papers.models import QuestionPaper

# ── Test 1: Direct Supabase upload ────────────────────────────────────────────
print("=" * 50)
print("TEST 1: Direct Supabase upload")
name = "question_papers/debug_test.pdf"
url = f"{settings.SUPABASE_URL}/storage/v1/object/{settings.SUPABASE_BUCKET}/{name}"
headers = {
    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE}",
    "apikey": settings.SUPABASE_SERVICE_ROLE,
    "Content-Type": "application/pdf",
    "x-upsert": "true"
}
response = requests.post(url, headers=headers, data=b"%PDF-1.4 test")
print("Status:", response.status_code)
print("Response:", response.text)

# ── Test 2: Check existing paper record ───────────────────────────────────────
print("=" * 50)
print("TEST 2: Existing paper record")
try:
    p = QuestionPaper.objects.get(id=2)
    print("PDF name:", p.pdf.name)
    print("PDF URL:", p.pdf.storage.url(p.pdf.name))
except Exception as e:
    print("Error:", e)

# ── Test 3: Check env vars loaded ─────────────────────────────────────────────
print("=" * 50)
print("TEST 3: Env vars")
print("SUPABASE_URL:", settings.SUPABASE_URL)
print("SUPABASE_BUCKET:", settings.SUPABASE_BUCKET)
print("SUPABASE_KEY set:", bool(settings.SUPABASE_SERVICE_ROLE))