from django.urls import path
from . import views

urlpatterns = [
    path('overview.php', views.OverviewView.as_view()),
]
