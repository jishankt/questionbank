from django.contrib import admin
from .models import ClassLevel, Subject, QuestionPaper


@admin.register(ClassLevel)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "class_level")
    list_filter = ("class_level",)


@admin.register(QuestionPaper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "year", "uploaded_by")
    list_filter = ("year", "subject")
    search_fields = ("title",)