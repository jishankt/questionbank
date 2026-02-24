import os
from django.core.files.storage import Storage
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET = os.getenv("SUPABASE_BUCKET")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseStorage(Storage):

    def _save(self, name, content):
        file_bytes = content.read()

        supabase.storage.from_(BUCKET).upload(
            name,
            file_bytes,
            {"content-type": "application/pdf"}
        )

        return name

    def url(self, name):
        return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{name}"