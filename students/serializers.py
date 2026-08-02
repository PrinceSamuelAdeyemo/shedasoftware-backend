from rest_framework import serializers
from .models import Student


class StudentListSerializer(serializers.ModelSerializer):
    student_id = serializers.ReadOnlyField()
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    full_name = serializers.SerializerMethodField()
    program_title = serializers.CharField(source='program.program_title', read_only=True)
    program_code = serializers.CharField(source='program.program_code', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'full_name', 'first_name', 'last_name',
            'email', 'program_title', 'program_code', 'status', 'fees_status', 'enrollment_date',
        ]

    def get_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'.strip()


class StudentDetailSerializer(serializers.ModelSerializer):
    student_id = serializers.ReadOnlyField()
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    full_name = serializers.SerializerMethodField()
    program_title = serializers.CharField(source='program.program_title', read_only=True)
    program_code = serializers.CharField(source='program.program_code', read_only=True)
    program_duration = serializers.CharField(source='program.duration', read_only=True)
    program_price = serializers.DecimalField(source='program.price', max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'full_name', 'first_name', 'last_name', 'email',
            'program_title', 'program_code', 'program_duration', 'program_price',
            'status', 'fees_status', 'enrollment_date',
        ]

    def get_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'.strip()
