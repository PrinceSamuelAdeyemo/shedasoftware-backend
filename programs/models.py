import random
import string
from django.db import models


def generate_program_code():
    return 'PRG-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Program(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('installment', 'Installment'),
        ('full', 'One Time Payment'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    program_code = models.CharField(max_length=20, unique=True, blank=True)
    program_title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.CharField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='full')
    duration = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    # Stored as a JSON list of instructor names/IDs from the frontend
    instructors = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.program_code:
            code = generate_program_code()
            while Program.objects.filter(program_code=code).exists():
                code = generate_program_code()
            self.program_code = code
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.program_code} – {self.program_title}'


class AssessmentQuestion(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.program.program_code}] {self.question[:60]}'
