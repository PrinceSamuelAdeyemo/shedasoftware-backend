from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import User, OTPToken
from .serializers import (
    LoginSerializer,
    RequestPasswordResetSerializer,
    SetPasswordSerializer,
    VerifyEmailSerializer,
)
from applications.models import Application
from applications.serializers import ApplicationSignupSerializer


def ok(data):
    return Response({'status': True, 'data': data})


def err(message, http_status=status.HTTP_400_BAD_REQUEST):
    return Response({'status': False, 'message': message}, status=http_status)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return err(serializer.errors)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)

        if user is None:
            return err('Invalid email or password.')

        token, _ = Token.objects.get_or_create(user=user)

        data = {
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
        }

        # Include applicant_id if the user has an application (student/applicant role)
        application = Application.objects.filter(email=user.email).order_by('-created_at').first()
        if application:
            data['applicant_id'] = application.applicant_id

        return ok(data)


class RequestPasswordResetView(APIView):

    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return err(serializer.errors)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal whether the email exists
            return ok({'message': 'If that email is registered, an OTP has been sent.'})

        # Invalidate old OTPs
        OTPToken.objects.filter(user=user, purpose='password_reset', is_used=False).update(is_used=True)

        otp_token = OTPToken.objects.create(user=user, purpose='password_reset')

        send_mail(
            subject='Sheda Academy – Password Reset OTP',
            message=(
                f'Hello {user.first_name or user.email},\n\n'
                f'Your OTP for password reset is: {otp_token.otp}\n\n'
                f'It expires in {settings.OTP_EXPIRY_MINUTES} minutes.\n\n'
                'If you did not request this, ignore this email.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        return ok({'message': 'If that email is registered, an OTP has been sent.'})


class SetPasswordView(APIView):

    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return err(serializer.errors)

        email = serializer.validated_data['email']
        otp_value = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return err('Invalid request.')

        otp_token = OTPToken.objects.filter(
            user=user, otp=otp_value, purpose='password_reset', is_used=False
        ).order_by('-created_at').first()

        if otp_token is None or not otp_token.is_valid:
            return err('Invalid or expired OTP.')

        user.set_password(new_password)
        user.save()
        otp_token.is_used = True
        otp_token.save()

        return ok({'message': 'Password updated successfully.'})


class VerifyEmailView(APIView):

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return err(serializer.errors)

        email = serializer.validated_data['email']
        otp_value = serializer.validated_data['otp']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return err('Invalid request.')

        otp_token = OTPToken.objects.filter(
            user=user, otp=otp_value, purpose='email_verify', is_used=False
        ).order_by('-created_at').first()

        if otp_token is None or not otp_token.is_valid:
            return err('Invalid or expired OTP.')

        user.is_email_verified = True
        user.save()
        otp_token.is_used = True
        otp_token.save()

        return ok({'message': 'Email verified successfully.'})


class ApplicationSignupView(APIView):
    """
    Creates the application record and a User account for the applicant.
    """

    def post(self, request):
        serializer = ApplicationSignupSerializer(data=request.data)
        if not serializer.is_valid():
            return err(serializer.errors)

        data = serializer.validated_data
        email = data['email']

        # Create or get the user account
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'role': 'applicant',
            }
        )
        if created:
            # Set a temporary unusable password, the user sets one via email link
            user.set_unusable_password()
            user.save()

            # Send email verification OTP
            otp_token = OTPToken.objects.create(user=user, purpose='email_verify')
            send_mail(
                subject='Sheda Academy – Verify Your Email',
                message=(
                    f'Hello {user.first_name},\n\n'
                    f'Thank you for applying to Sheda Academy!\n\n'
                    f'Your email verification OTP is: {otp_token.otp}\n\n'
                    f'It expires in {settings.OTP_EXPIRY_MINUTES} minutes.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )

        # Find the program
        from programs.models import Program
        try:
            program = Program.objects.get(program_code=data['program_code'])
        except Program.DoesNotExist:
            return err('Program not found.')

        # Create the application
        from applications.models import Application, AssessmentAnswer
        application = Application.objects.create(
            program=program,
            email=email,
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data.get('middle_name', ''),
            phone_number=data['phone_number'],
            date_birth=data.get('date_birth'),
            state_origin=data['state_origin'],
            state_residence=data['state_residence'],
            highest_degree=data['highest_degree'],
            school_obtained=data.get('school_obtained', ''),
            program_type=data.get('program_type', ''),
        )

        for answer in data.get('assessment_answers', []):
            AssessmentAnswer.objects.create(
                application=application,
                question=answer['question'],
                answer=answer['answer'],
            )

        return ok({'applicant_id': application.applicant_id})
