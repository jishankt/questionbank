from django.contrib.auth.models import User
from django.db import models

class StudentProfile(models.Model):

    CLASS_CHOICES = [
        ('10', '10th'),
        ('11', '11th'),
        ('12', '12th'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES)
    school_name = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username
