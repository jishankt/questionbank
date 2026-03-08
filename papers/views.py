from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import VisitorCount

from .models import ClassLevel, Subject, QuestionPaper
from .serializers import (
    ClassLevelSerializer,
    SubjectSerializer,
    QuestionPaperSerializer
)


# =====================================
# GET ALL CLASSES
# =====================================
@api_view(["GET"])
def get_visitor_count(request):
    """Return current visitor count without incrementing."""
    from .models import VisitorCount
    return Response({"count": VisitorCount.get_count()})


@api_view(["POST"])
def increment_visitor(request):
    """Increment visitor count and return new value."""
    from .models import VisitorCount
    count = VisitorCount.increment()
    return Response({"count": count})

@api_view(["GET"])
def get_classes(request):

    classes = ClassLevel.objects.all()

    serializer = ClassLevelSerializer(
        classes,
        many=True
    )

    return Response(serializer.data)


# =====================================
# GET SUBJECTS OF A CLASS
# =====================================

@api_view(["GET"])
def get_subjects(request, class_id):

    subjects = Subject.objects.filter(
        class_level_id=class_id
    )

    serializer = SubjectSerializer(
        subjects,
        many=True
    )

    return Response(serializer.data)


# =====================================
# GET PAPERS OF A SUBJECT
# =====================================

@api_view(["GET"])
def get_papers(request, subject_id):

    papers = QuestionPaper.objects.filter(
        subject_id=subject_id
    ).order_by("-year")

    serializer = QuestionPaperSerializer(
        papers,
        many=True,
        context={"request": request}
    )

    return Response(serializer.data)


# =====================================
# UPLOAD QUESTION PAPER
# =====================================

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_paper(request):

    serializer = QuestionPaperSerializer(
        data=request.data,
        context={"request": request}
    )

    if serializer.is_valid():

        user = request.user if request.user.is_authenticated else None

        serializer.save(uploaded_by=user)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )