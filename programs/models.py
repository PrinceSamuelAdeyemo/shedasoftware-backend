import random
import string
from django.db import models


# def generate_program_code():
#     return 'PRG-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Program(models.Model):

    DURATION_CHOICE = [
        ('1 month', '1 month'),
        ('3 months', '1 months'),
        ('4 months', '4 months'),
        ('6 months', '6 months'),
        ('12 months', '1 year'),
        ('18 months', ' 1 year 6 months'),
        ('24 months', '2 years'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    program_code = models.CharField(max_length=20, unique=True)
    program_title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField()
    # price = models.DecimalField(max_digits=12, decimal_places=2)
    # payment_type = models.CharField(max_length=20)
    duration = models.CharField(max_length=100, choices=DURATION_CHOICE, default='12 months')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    # Stored as a JSON list of instructor names/IDs from the frontend
    instructors = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        #if not self.program_code:
            #code = generate_program_code()
            #while Program.objects.filter(program_code=code).exists():
            #    code = generate_program_code()
            #self.program_code = code
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.program_code} – {self.program_title}'

class PaymentPlan(models.Model):

    PLAN_TYPES_CHOICES = [
        ("FULL", "Full Payment"),
        ("MONTHLY", "Every Month"),
        ("3_MONTHS", "Every 3 Months"),
        ("6_MONTHS", "Every 6 Months"),
    ]

    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="payment_plans"
    )

    plan_type = models.CharField(
        max_length=20,
        choices=PLAN_TYPES_CHOICES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["program", "plan_type"],
                name="unique_program_payment_plan"
            )
        ]

    def __str__(self):
        return f"{self.program.title} - {self.get_plan_display()}"
    


class Assessment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="assessments"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class AssessmentQuestion(models.Model):

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(
            auto_now_add=True
    )

    def __str__(self):
        return self.question


class AssessmentAnswer(models.Model):
    question = models.ForeignKey(
        AssessmentQuestion,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    text_answer = models.TextField(
        blank=True
    )
    answered_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.attempt.applicant} - {self.question}"