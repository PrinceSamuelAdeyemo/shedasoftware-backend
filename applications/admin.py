from django.contrib import admin
from .models import Application, AssessmentAnswer


class AssessmentAnswerInline(admin.TabularInline):
    model = AssessmentAnswer
    extra = 0
    readonly_fields = ['question', 'answer']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant_id', 'full_name', 'email', 'program', 'status', 'created_at']
    list_filter = ['status', 'program']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['created_at']
    inlines = [AssessmentAnswerInline]

    def applicant_id(self, obj):
        return obj.applicant_id
    applicant_id.short_description = 'Applicant ID'

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'


@admin.register(AssessmentAnswer)
class AssessmentAnswerAdmin(admin.ModelAdmin):
    list_display = ['application', 'question']
    search_fields = ['application__email', 'question']
