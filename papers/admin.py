from django.contrib import admin
from django.utils.html import format_html
from .models import ClassLevel, Subject, QuestionPaper


# -----------------------------
# CLASS LEVEL ADMIN
# -----------------------------
@admin.register(ClassLevel)
class ClassAdmin(admin.ModelAdmin):

    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


# -----------------------------
# SUBJECT ADMIN
# -----------------------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "class_level")
    list_filter = ("class_level",)
    search_fields = ("name",)
    ordering = ("class_level",)


# -----------------------------
# QUESTION PAPER ADMIN
# -----------------------------
@admin.register(QuestionPaper)
class PaperAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "subject",
        "year",
        "uploaded_by",
        "uploaded_at",
        "view_pdf",
    )

    list_filter = ("year", "subject")
    search_fields = ("title", "subject__name")
    ordering = ("-uploaded_at",)

    readonly_fields = ("uploaded_at",)

    # Show PDF link in admin
    def view_pdf(self, obj):
        if obj.pdf:
            return format_html(
                '<a href="{}" target="_blank">📄 View PDF</a>',
                obj.pdf.url
            )
        return "No File"

    view_pdf.short_description = "PDF"