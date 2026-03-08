import os, sys, django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "questionbank.settings")
django.setup()

from django.core.files.base import ContentFile
from papers.models import QuestionPaper, Subject
from papers.supabase_storage import SupabaseStorage

# ── Check storage on the model field ─────────────────────────────────────────
print("=" * 50)
print("Storage class on QuestionPaper.pdf field:")
field = QuestionPaper._meta.get_field("pdf")
print(type(field.storage))
print(field.storage.__class__.__name__)

# ── Check DEFAULT_FILE_STORAGE ────────────────────────────────────────────────
from django.conf import settings
print("=" * 50)
print("DEFAULT_FILE_STORAGE:", settings.DEFAULT_FILE_STORAGE)

# ── Try saving via the model directly ────────────────────────────────────────
print("=" * 50)
print("Attempting model-level save with SupabaseStorage...")

subject = Subject.objects.first()
if not subject:
    print("ERROR: No subject found! Create one in admin first.")
else:
    print("Using subject:", subject)
    paper = QuestionPaper(
        title="Storage Test Paper",
        year=2024,
        subject=subject,
    )
    # Save file via the model's file field
    paper.pdf.save(
        "storage_test.pdf",
        ContentFile(b"%PDF-1.4 storage test"),
        save=False
    )
    print("PDF name after save:", paper.pdf.name)
    print("PDF URL:", paper.pdf.url)
    paper.save()
    print("Record saved! ID:", paper.id)
    print("Final URL:", QuestionPaper.objects.get(id=paper.id).pdf.storage.url(
        QuestionPaper.objects.get(id=paper.id).pdf.name
    ))