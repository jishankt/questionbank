from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import QuestionPaper, Subject
from .forms import PaperUploadForm
from accounts.models import StudentProfile


# ---------------- Student Subject List ----------------
@login_required
def paper_list(request):

    # Get student profile safely
    student = get_object_or_404(StudentProfile, user=request.user)

    # Get class from request or student profile
    class_name = request.GET.get("class") or student.class_name

    subjects = Subject.objects.filter(class_name=class_name)

    return render(request, 'student_subjects.html', {
        'subjects': subjects,
        'class_name': class_name
    })


# ---------------- Uploader Dashboard ----------------
@login_required
def uploader_dashboard(request):

    if not request.user.is_staff:
        return redirect('paper_list')

    papers = QuestionPaper.objects.all().order_by('-year')
    students = StudentProfile.objects.select_related('user')

    return render(request, 'uploader_dashboard.html', {
        'papers': papers,
        'students': students
    })


# ---------------- Upload Paper ----------------
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import QuestionPaper, Subject

@login_required
def upload_paper(request):
    if not request.user.is_staff:
        return redirect('paper_list')

    subjects = Subject.objects.all()

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        year = request.POST.get('year')
        pdf_file = request.FILES.get('pdf_file')

        subject = Subject.objects.get(id=subject_id)

        QuestionPaper.objects.create(
            subject=subject,
            class_name=subject.class_name,  # automatically set
            year=year,
            pdf_file=pdf_file
        )

        return redirect('uploader_dashboard')

    return render(request, 'upload_paper.html', {'subjects': subjects})



# ---------------- Delete Paper ----------------
@login_required
def delete_paper(request, id):

    if not request.user.is_staff:
        return redirect('paper_list')

    paper = get_object_or_404(QuestionPaper, id=id)

    if request.method == "POST":
        paper.delete()
        return redirect('uploader_dashboard')

    return redirect('uploader_dashboard')


# ---------------- Student Papers ----------------
@login_required
def student_papers(request, subject_id):

    student = get_object_or_404(StudentProfile, user=request.user)

    papers = QuestionPaper.objects.filter(
        subject_id=subject_id,
        subject__class_name=student.class_name
    ).order_by('-year')

    subject = get_object_or_404(Subject, id=subject_id)

    return render(request, 'student_papers.html', {
        'papers': papers,
        'subject': subject
    })
