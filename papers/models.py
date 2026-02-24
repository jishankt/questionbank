from django.db import models
from django.contrib.auth.models import User


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
    pdf = models.FileField(upload_to="question_papers/")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.year}"