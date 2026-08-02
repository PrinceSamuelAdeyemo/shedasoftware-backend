from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from students.models import Student
from applications.models import Application
from programs.models import Program


def ok(data):
    return Response({'status': True, 'data': data})


class OverviewView(APIView):
    """
    This will returns aggregate stats for the admin dashboard.
    timeFrame is number of days to look back (e.g. 7, 30, 365).
    """

    def get(self, request):
        try:
            time_frame = int(request.query_params.get('timeFrame', 14))
        except ValueError:
            time_frame = 14

        since = timezone.now() - timezone.timedelta(days=time_frame)

        # All-time counts
        active_students = Student.objects.filter(status='student').count()
        graduates = Student.objects.filter(status='graduate').count()
        outliers = Student.objects.filter(status='outlier').count()
        total_programs = Program.objects.filter(status='active').count()

        # Within the selected time frame
        new_applicants = Application.objects.filter(created_at__gte=since).count()
        new_students = Student.objects.filter(enrollment_date__gte=since.date()).count()
        accepted_applicants = Application.objects.filter(
            status='accepted', created_at__gte=since
        ).count()
        rejected_applicants = Application.objects.filter(
            status='rejected', created_at__gte=since
        ).count()
        awaiting_applicants = Application.objects.filter(
            status='awaiting', created_at__gte=since
        ).count()

        total_students = active_students + graduates + outliers
        graduation_rate = (
            round((graduates / total_students) * 100) if total_students > 0 else 0
        )

        return ok({
            'active_students': active_students,
            'graduates': graduates,
            'outliers': outliers,
            'total_programs': total_programs,
            'graduation_rate': graduation_rate,
            # Time-frame specific
            'applicants': new_applicants,
            'new_students': new_students,
            'accepted_applicants': accepted_applicants,
            'rejected_applicants': rejected_applicants,
            'awaiting_applicants': awaiting_applicants,
            'time_frame_days': time_frame,
        })
