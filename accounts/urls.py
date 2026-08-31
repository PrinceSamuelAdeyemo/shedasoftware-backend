from django.urls import path
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('reset.password.php', views.RequestPasswordResetView.as_view()),
    path('set-password', views.SetPasswordView.as_view()),
    path('verify.email.password.php', views.VerifyEmailView.as_view()),
    path('application.signup', views.ApplicationSignupView.as_view()),
]
