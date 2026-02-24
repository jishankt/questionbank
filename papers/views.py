from django.shortcuts import render, get_object_or_404
from .models import Subject, QuestionPaper, ClassLevel


def home(request):
    classes = ClassLevel.objects.all()
    return render(request, "papers/home.html", {"classes": classes})


def subjects(request, class_no):
    class_level = get_object_or_404(ClassLevel, name=class_no)

    subjects = Subject.objects.filter(class_level=class_level)

    return render(request, "papers/subjects.html", {
        "subjects": subjects,
        "class_level": class_level
    })


def papers(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    papers = subject.papers.all()

    return render(request, "papers/papers.html", {
        "subject": subject,
        "papers": papers
    })