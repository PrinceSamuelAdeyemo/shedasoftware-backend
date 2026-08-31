from django.contrib import admin
from .models import Program, Assessment, AssessmentQuestion, AssessmentAnswer


class AssessmentQuestionInline(admin.TabularInline):
    model = AssessmentQuestion
    extra = 1


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['program_code', 'program_title', 'duration', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['program_code', 'program_title']
    readonly_fields = ['created_at']
    #inlines = [AssessmentQuestionInline]


@admin.register(Assessment)
class AssessmmentAdmin(admin.ModelAdmin):
    list_display = ['program', 'title', 'created_at']
    search_fields = ['program', 'title']

@admin.register(AssessmentQuestion)
class AssessmentQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'assessment', 'question', 'created_at']
    list_filter = ['assessment']
    search_fields = ['question']

@admin.register(AssessmentAnswer)
class AssessmentAnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'text_answer', 'answered_at']
    list_filter = ['question']
    search_fields = ['question']