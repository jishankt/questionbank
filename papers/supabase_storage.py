import requests
from django.core.files.storage import Storage
from django.conf import settings


class SupabaseStorage(Storage):

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE}",
            "apikey": settings.SUPABASE_SERVICE_ROLE,
        }

    # ------------------------------------------------------------------
    # FIX 1: Correct upload endpoint — /object/{bucket}/{name}
    #         Added Content-Type header so Supabase accepts the file
    #         Added upsert header so re-uploads don't 409
    # ------------------------------------------------------------------
    def _save(self, name, content):
        url = (
            f"{settings.SUPABASE_URL}/storage/v1/object/"
            f"{settings.SUPABASE_BUCKET}/{name}"
        )

        headers = self._get_headers()
        headers["Content-Type"] = "application/pdf"
        headers["x-upsert"] = "true"          # overwrite if re-uploaded

        response = requests.post(url, headers=headers, data=content.read())

        if response.status_code not in [200, 201]:
            raise Exception(
                f"Supabase upload failed [{response.status_code}]: {response.text}"
            )
        return name

    # ------------------------------------------------------------------
    # FIX 2: Public URL for the frontend
    # ------------------------------------------------------------------
    def url(self, name):
        return (
            f"{settings.SUPABASE_URL}/storage/v1/object/public/"
            f"{settings.SUPABASE_BUCKET}/{name}"
        )

    # ------------------------------------------------------------------
    # FIX 3: Required Storage API methods Django/admin calls internally
    # ------------------------------------------------------------------
    def exists(self, name):
        """Check if file exists in Supabase bucket."""
        url = (
            f"{settings.SUPABASE_URL}/storage/v1/object/info/public/"
            f"{settings.SUPABASE_BUCKET}/{name}"
        )
        response = requests.head(url, headers=self._get_headers())
        return response.status_code == 200

    def delete(self, name):
        """Delete a file from Supabase bucket."""
        url = (
            f"{settings.SUPABASE_URL}/storage/v1/object/"
            f"{settings.SUPABASE_BUCKET}"
        )
        response = requests.delete(
            url,
            headers={**self._get_headers(), "Content-Type": "application/json"},
            json={"prefixes": [name]},
        )
        return response.status_code in [200, 204]

    def _open(self, name, mode="rb"):
        """Download a file from Supabase (needed by Django internally)."""
        from django.core.files.base import ContentFile
        url = self.url(name)
        response = requests.get(url)
        if response.status_code != 200:
            raise FileNotFoundError(f"File not found in Supabase: {name}")
        return ContentFile(response.content, name=name)

    def size(self, name):
        """Return file size."""
        url = (
            f"{settings.SUPABASE_URL}/storage/v1/object/info/public/"
            f"{settings.SUPABASE_BUCKET}/{name}"
        )
        response = requests.head(url, headers=self._get_headers())
        content_length = response.headers.get("Content-Length")
        return int(content_length) if content_length else 0
