from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'user', 'program', 'status', 'fees_status', 'enrollment_date']
    list_filter = ['status', 'fees_status', 'program']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['enrollment_date']

    def student_id(self, obj):
        return obj.student_id
    student_id.short_description = 'Student ID'
