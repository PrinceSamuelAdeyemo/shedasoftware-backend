from rest_framework import serializers
from .models import Application, AssessmentAnswer


class AssessmentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentAnswer
        fields = ['question', 'answer']


class ApplicationSignupSerializer(serializers.Serializer):
    """Used by AccountsView.ApplicationSignupView to validate incoming data."""
    email = serializers.EmailField()
    program_code = serializers.CharField()
    program = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField(required=False, allow_blank=True, default='')
    phone_number = serializers.CharField()
    date_birth = serializers.DateField(required=False, allow_null=True, default=None)
    state_origin = serializers.CharField()
    state_residence = serializers.CharField()
    highest_degree = serializers.CharField()
    school_obtained = serializers.CharField(required=False, allow_blank=True, default='')
    program_type = serializers.CharField(required=False, allow_blank=True, default='')
    assessment_answers = AssessmentAnswerSerializer(many=True, required=False, default=list)


class ApplicationListSerializer(serializers.ModelSerializer):
    applicant_id = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()
    program_title = serializers.CharField(source='program.program_title', read_only=True)
    program_code = serializers.CharField(source='program.program_code', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'applicant_id', 'full_name', 'email',
            'program_title', 'program_code', 'status', 'created_at',
        ]


class ApplicationDetailSerializer(serializers.ModelSerializer):
    applicant_id = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()
    program_title = serializers.CharField(source='program.program_title', read_only=True)
    program_code = serializers.CharField(source='program.program_code', read_only=True)
    assessment_answers = AssessmentAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'applicant_id', 'full_name', 'first_name', 'last_name', 'middle_name',
            'email', 'phone_number', 'date_birth', 'state_origin', 'state_residence',
            'highest_degree', 'school_obtained', 'program_type',
            'program_title', 'program_code', 'status', 'assessment_answers', 'created_at',
        ]


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']
