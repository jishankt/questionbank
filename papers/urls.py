from django.urls import path
from . import views

urlpatterns = [

    path("classes/", views.get_classes),

    path("subjects/<int:class_id>/", views.get_subjects),

    path("papers/<int:subject_id>/", views.get_papers),

    path("upload-paper/", views.upload_paper),

    path("visitors/", views.get_visitor_count),

    path("visitors/increment/", views.increment_visitor),

    path("papers/count/", views.paper_count),

]