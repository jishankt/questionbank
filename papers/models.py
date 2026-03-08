from django.db import models
from django.contrib.auth.models import User
from papers.supabase_storage import SupabaseStorage


class ClassLevel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Subject(models.Model):
    class_level = models.ForeignKey(
        ClassLevel,
        on_delete=models.CASCADE,
        related_name="subjects"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.class_level})"


class QuestionPaper(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="papers"
    )

    title = models.CharField(max_length=200)
    year = models.IntegerField()

    # FIX: Explicitly pass SupabaseStorage so Django doesn't fall back
    # to FileSystemStorage via lazy DefaultStorage caching
    pdf = models.FileField(
        upload_to="question_papers/",
        storage=SupabaseStorage()
    )

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.year}"





class VisitorCount(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Visitors: {self.count}"