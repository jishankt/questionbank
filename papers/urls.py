from django.urls import path
from . import views

urlpatterns = [
    path('', views.paper_list, name='paper_list'),
    path('papers/<str:subject_id>/', views.student_papers, name='student_papers'),

    path('dashboard/', views.uploader_dashboard, name='uploader_dashboard'),
    path('upload/', views.upload_paper, name='upload_paper'),
    path('delete/<int:id>/', views.delete_paper, name='delete_paper'),
]
