from django.db import models
from django.core.exceptions import ValidationError


def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError("Only PDF files allowed")

    if value.size > 5 * 1024 * 1024:
        raise ValidationError("File too large (Max 5MB)")


# ---------- Subject Model ----------
class Subject(models.Model):

    CLASS_CHOICES = [
        ('10', '10th'),
        ('11', '11th'),
        ('12', '12th'),
    ]

    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.class_name})"


# ---------- Question Paper Model ----------
class QuestionPaper(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=10)
    year = models.IntegerField()
    pdf_file = models.FileField(upload_to='papers/', validators=[validate_pdf])

    def __str__(self):
        return f"{self.subject.name} - {self.year}"
