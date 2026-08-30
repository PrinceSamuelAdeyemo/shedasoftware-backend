from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Program, AssessmentQuestion
from .serializers import (
    ProgramDetailSerializer,
    ProgramListSerializer,
    ProgramCreateSerializer,
    AssessmentQuestionSerializer,
    AssessmentQuestionCreateSerializer,
)


def ok(data):
    return Response({'status': True, 'data': data})


def err(message, http_status=status.HTTP_400_BAD_REQUEST):
    return Response({'status': False, 'message': message}, status=http_status)


class ProgramDetailView(APIView):

    def get(self, request):
        #code = request.query_params.get('code')
        #if not code:
        #    return err('program_code is required.')
        try:
            #program = Program.objects.get(program_code=code)
            program = Program.objects.all()
        except Program.DoesNotExist:
            return err('Program not found.', status.HTTP_404_NOT_FOUND)
        return ok(ProgramDetailSerializer(program).data)

class ProgramListView(APIView):

    def get(self, request):
        program = Program.objects.all()
        return ok(ProgramListSerializer(program, many=True).data)

class AssessmentQuestionsView(APIView):

    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return err('program_code is required.')
        try:
            program = Program.objects.get(program_code=code)
        except Program.DoesNotExist:
            return err('Program not found.', status.HTTP_404_NOT_FOUND)
        questions = AssessmentQuestion.objects.filter(program=program)
        return ok(AssessmentQuestionSerializer(questions, many=True).data)


class AdminProgramListView(APIView):
    """
    Query params: search, paymentType, page, limit
    """

    def get(self, request):
        qs = Program.objects.all().order_by('-created_at')
        print('hello')
        search = request.query_params.get('search', '').strip()
        print('search params', search)
        payment_type = request.query_params.get('paymentType', '').strip()

        if search:
            qs = qs.filter(
                Q(program_title__icontains=search) |
                Q(program_code__icontains=search)
            )
        if payment_type:
            qs = qs.filter(payment_type=payment_type)

        try:
            page = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', 10))
        except ValueError:
            page, limit = 1, 10

        start = (page - 1) * limit
        end = start + limit
        total = qs.count()

        return ok({
            'programs': ProgramListSerializer(qs[start:end], many=True).data,
            'total': total,
            'page': page,
            'limit': limit,
        })


class AdminProgramCreateView(APIView):

    def post(self, request):
        serializer = ProgramCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return err(serializer.errors)
        program = serializer.save()
        return ok(ProgramDetailSerializer(program).data)


class AssessmentQuestionAdminView(APIView):

    def get(self, request):
        program_code = request.query_params.get('program_code', '')
        qs = AssessmentQuestion.objects.all().order_by('id')
        if program_code:
            qs = qs.filter(program__program_code=program_code)
        return ok(AssessmentQuestionSerializer(qs, many=True).data)

    def post(self, request):
        # Accept a single question or a list
        data = request.data
        if isinstance(data, list):
            serializer = AssessmentQuestionCreateSerializer(data=data, many=True)
        else:
            serializer = AssessmentQuestionCreateSerializer(data=data)

        if not serializer.is_valid():
            return err(serializer.errors)

        result = serializer.save()
        if isinstance(result, list):
            return ok(AssessmentQuestionSerializer(result, many=True).data)
        return ok(AssessmentQuestionSerializer(result).data)


class AssessmentQuestionDetailView(APIView):

    def _get_question(self, pk):
        try:
            return AssessmentQuestion.objects.get(pk=pk)
        except AssessmentQuestion.DoesNotExist:
            return None

    def get(self, request, pk):
        question = self._get_question(pk)
        if question is None:
            return err('Question not found.', status.HTTP_404_NOT_FOUND)
        return ok(AssessmentQuestionSerializer(question).data)

    def put(self, request, pk):
        question = self._get_question(pk)
        if question is None:
            return err('Question not found.', status.HTTP_404_NOT_FOUND)
        serializer = AssessmentQuestionSerializer(question, data=request.data, partial=True)
        if not serializer.is_valid():
            return err(serializer.errors)
        serializer.save()
        return ok(serializer.data)

    def delete(self, request, pk):
        question = self._get_question(pk)
        if question is None:
            return err('Question not found.', status.HTTP_404_NOT_FOUND)
        question.delete()
        return ok({'message': 'Question deleted.'})
