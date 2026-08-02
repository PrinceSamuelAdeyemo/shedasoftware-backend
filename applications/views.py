from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Application
from .serializers import (
    ApplicationListSerializer,
    ApplicationDetailSerializer,
    ApplicationStatusUpdateSerializer,
)


def ok(data):
    return Response({'status': True, 'data': data})


def err(message, http_status=status.HTTP_400_BAD_REQUEST):
    return Response({'status': False, 'message': message}, status=http_status)


class ApplicantListView(APIView):
    """
    Query params: search, status (awaiting/accepted/rejected), page, limit
    """

    def get(self, request):
        qs = Application.objects.all().order_by('-created_at')

        search = request.query_params.get('search', '').strip()
        app_status = request.query_params.get('status', '').strip()

        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        if app_status:
            qs = qs.filter(status=app_status)

        try:
            page = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', 20))
        except ValueError:
            page, limit = 1, 20

        start = (page - 1) * limit
        total = qs.count()

        return ok({
            'applicants': ApplicationListSerializer(qs[start:start + limit], many=True).data,
            'total': total,
            'page': page,
            'limit': limit,
        })


class ApplicantDetailView(APIView):

    def _get_application(self, pk):
        try:
            return Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return None

    def get(self, request, pk):
        application = self._get_application(pk)
        if application is None:
            return err('Applicant not found.', status.HTTP_404_NOT_FOUND)
        return ok(ApplicationDetailSerializer(application).data)

    def patch(self, request, pk):
        """Accept or reject an applicant: PATCH with {"status": "accepted"|"rejected"}"""
        application = self._get_application(pk)
        if application is None:
            return err('Applicant not found.', status.HTTP_404_NOT_FOUND)

        serializer = ApplicationStatusUpdateSerializer(application, data=request.data, partial=True)
        if not serializer.is_valid():
            return err(serializer.errors)

        serializer.save()
        return ok(ApplicationDetailSerializer(application).data)
