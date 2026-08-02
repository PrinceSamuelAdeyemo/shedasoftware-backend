from rest_framework import serializers
from .models import Program, AssessmentQuestion


class AssessmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQuestion
        fields = ['id', 'question']


class ProgramDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = [
            'id', 'program_code', 'program_title', 'description',
            'cover_image', 'price', 'payment_type', 'duration',
            'status', 'instructors', 'created_at',
        ]


class ProgramListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = [
            'id', 'program_code', 'program_title', 'description',
            'cover_image', 'price', 'payment_type', 'duration',
            'status', 'created_at',
        ]


class ProgramCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = [
            'program_title', 'description', 'cover_image',
            'price', 'payment_type', 'duration', 'status', 'instructors',
        ]


class AssessmentQuestionCreateSerializer(serializers.ModelSerializer):
    program_code = serializers.CharField(write_only=True)

    class Meta:
        model = AssessmentQuestion
        fields = ['id', 'program_code', 'question']

    def create(self, validated_data):
        from .models import Program
        program_code = validated_data.pop('program_code')
        program = Program.objects.get(program_code=program_code)
        return AssessmentQuestion.objects.create(program=program, **validated_data)
