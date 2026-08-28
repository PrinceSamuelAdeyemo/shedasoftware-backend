from django.db import models


class Student(models.Model):
    STATUS_CHOICES = [
        ('student', 'Student'),
        ('graduate', 'Graduate'),
        ('outlier', 'Outlier'),
    ]
    FEES_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]

    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='student_profile')
    program = models.ManyToManyField('programs.Program', related_name='student_programs', blank=True)
    #program = models.ForeignKey('programs.Program', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='student')
    fees_status = models.CharField(max_length=20, choices=FEES_CHOICES, default='unpaid')
    enrollment_date = models.DateField(auto_now_add=True)

    @property
    def student_id(self):
        return f'STU-{self.id:07d}'

    def __str__(self):
        return f'{self.user.email} – {self.get_status_display()}'
