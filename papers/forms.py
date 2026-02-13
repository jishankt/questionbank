from django import forms
from .models import QuestionPaper

class PaperUploadForm(forms.ModelForm):

    class Meta:
        model = QuestionPaper
        fields = ['subject', 'year', 'pdf_file']
