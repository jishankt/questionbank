from rest_framework import serializers
from .models import ClassLevel, Subject, QuestionPaper


# =====================================
# CLASS SERIALIZER
# =====================================

class ClassLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassLevel
        fields = ["id", "name"]


# =====================================
# SUBJECT SERIALIZER
# =====================================

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ["id", "name", "class_level"]


# =====================================
# QUESTION PAPER SERIALIZER
# FIX: Removed duplicate import, clean get_pdf logic
# =====================================

class QuestionPaperSerializer(serializers.ModelSerializer):

    subject_name = serializers.CharField(source="subject.name", read_only=True)
    pdf = serializers.SerializerMethodField()

    class Meta:
        model = QuestionPaper
        fields = [
            "id",
            "title",
            "year",
            "pdf",
            "subject",
            "subject_name",
            "uploaded_by",
            "uploaded_at",
        ]
        read_only_fields = ["uploaded_by", "uploaded_at"]

    def get_pdf(self, obj):
        """
        Returns a fully accessible public URL.
        SupabaseStorage.url() returns the Supabase public URL directly.
        Falls back to a local absolute URL in dev mode.
        """
        if not obj.pdf:
            return None

        try:
            # SupabaseStorage.url() returns the public CDN URL
            return obj.pdf.storage.url(obj.pdf.name)
        except Exception:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.pdf.url)
            return obj.pdf.url
