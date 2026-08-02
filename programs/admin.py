from django.contrib import admin
from .models import Program, AssessmentQuestion


class AssessmentQuestionInline(admin.TabularInline):
    model = AssessmentQuestion
    extra = 1


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['program_code', 'program_title', 'payment_type', 'price', 'duration', 'status', 'created_at']
    list_filter = ['payment_type', 'status']
    search_fields = ['program_code', 'program_title']
    readonly_fields = ['program_code', 'created_at']
    inlines = [AssessmentQuestionInline]


@admin.register(AssessmentQuestion)
class AssessmentQuestionAdmin(admin.ModelAdmin):
    list_display = ['program', 'question', 'created_at']
    list_filter = ['program']
    search_fields = ['question', 'program__program_title']
