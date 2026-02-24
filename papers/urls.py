from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("class/<int:class_no>/", views.subjects, name="subjects"),
    path("subject/<int:subject_id>/", views.papers, name="papers"),
]