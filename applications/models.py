from django.db import models


class Application(models.Model):
    STATUS_CHOICES = [
        ('awaiting', 'Awaiting'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    program = models.ForeignKey('programs.Program', on_delete=models.CASCADE, related_name='applications')
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20)
    date_birth = models.DateField(null=True, blank=True)
    state_origin = models.CharField(max_length=100)
    state_residence = models.CharField(max_length=100)
    highest_degree = models.CharField(max_length=200)
    school_obtained = models.CharField(max_length=200, blank=True)
    program_type = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='awaiting')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def applicant_id(self):
        return f'APP-{self.id:07d}'

    @property
    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return ' '.join(p for p in parts if p)

    def __str__(self):
        return f'{self.full_name} → {self.program.program_title} ({self.status})'


class AssessmentAnswer(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='assessment_answers')
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f'[{self.application.applicant_id}] {self.question[:50]}'
