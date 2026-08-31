from django.urls import path, include
from programs import views as program_views
from applications import views as application_views
from students import views as student_views
from dashboard import views as dashboard_views

urlpatterns = [
    # Auth (login, password reset, email verify, application signup)
    path('auth/', include('accounts.urls')),

    # Public: apply
    path('auth/application.signup', application_views.ApplicationCreateView.as_view()),

    # Public: program detail & assessment questions
    path('program.detail.php', program_views.ProgramDetailView.as_view()),
    path('assessment.php', program_views.AssessmentQuestionsView.as_view()),

    # Admin: programs
    path('admin/program/get.programs.php', program_views.AdminProgramListView.as_view()),
    path('admin/program/create.php', program_views.AdminProgramCreateView.as_view()),
    path('admin/program/create.php/', program_views.AdminProgramCreateView.as_view()),

    # Admin: assessment questions
    path('admin/assessment-questions/', program_views.AssessmentQuestionAdminView.as_view()),
    path('admin/assessment-questions/<int:pk>/', program_views.AssessmentQuestionDetailView.as_view()),

    # Admin: dashboard overview
    path('admin/dashboard/overview.php', dashboard_views.OverviewView.as_view()),

    # Admin: applicants
    path('admin/applicants/', application_views.ApplicantListView.as_view()),
    path('admin/applicants/<int:pk>/', application_views.ApplicantDetailView.as_view()),

    # Admin: students
    path('admin/students/', student_views.StudentListView.as_view()),
    path('admin/students/<int:pk>/', student_views.StudentDetailView.as_view()),

    # Student: own profile
    path('student/profile/', student_views.StudentProfileView.as_view()),

    # Programs
    path('programs.php', program_views.ProgramListView.as_view())
]
