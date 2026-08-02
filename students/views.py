from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Student
from .serializers import StudentListSerializer, StudentDetailSerializer


def ok(data):
    return Response({'status': True, 'data': data})


def err(message, http_status=status.HTTP_400_BAD_REQUEST):
    return Response({'status': False, 'message': message}, status=http_status)


class StudentListView(APIView):
    """GET /v1/api/admin/students/
    Query params: search, status (student/graduate/outlier), fees_status (paid/unpaid),
                  program_code, page, limit
    """

    def get(self, request):
        qs = Student.objects.select_related('user', 'program').all().order_by('-enrollment_date')

        search = request.query_params.get('search', '').strip()
        student_status = request.query_params.get('status', '').strip()
        fees_status = request.query_params.get('fees_status', '').strip()
        program_code = request.query_params.get('program_code', '').strip()

        if search:
            qs = qs.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search)
            )
        if student_status:
            qs = qs.filter(status=student_status)
        if fees_status:
            qs = qs.filter(fees_status=fees_status)
        if program_code:
            qs = qs.filter(program__program_code=program_code)

        try:
            page = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', 20))
        except ValueError:
            page, limit = 1, 20

        start = (page - 1) * limit
        total = qs.count()

        return ok({
            'students': StudentListSerializer(qs[start:start + limit], many=True).data,
            'total': total,
            'page': page,
            'limit': limit,
        })


class StudentDetailView(APIView):
    """GET /v1/api/admin/students/<pk>/"""

    def _get_student(self, pk):
        try:
            return Student.objects.select_related('user', 'program').get(pk=pk)
        except Student.DoesNotExist:
            return None

    def get(self, request, pk):
        student = self._get_student(pk)
        if student is None:
            return err('Student not found.', status.HTTP_404_NOT_FOUND)
        return ok(StudentDetailSerializer(student).data)

    def patch(self, request, pk):
        """Update student status or fees_status."""
        student = self._get_student(pk)
        if student is None:
            return err('Student not found.', status.HTTP_404_NOT_FOUND)

        allowed_fields = {'status', 'fees_status'}
        update_data = {k: v for k, v in request.data.items() if k in allowed_fields}
        for field, value in update_data.items():
            setattr(student, field, value)
        student.save()

        return ok(StudentDetailSerializer(student).data)


class StudentProfileView(APIView):
    """GET /v1/api/student/profile/
    Returns the currently logged-in student's profile.
    Requires Token authentication.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student = Student.objects.select_related('user', 'program').get(user=request.user)
        except Student.DoesNotExist:
            return err('Student profile not found.', status.HTTP_404_NOT_FOUND)
        return ok(StudentDetailSerializer(student).data)
