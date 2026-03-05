from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("register/", views.RegisterView.as_view()),
    path("verification_email/", views.VerifyEmail.as_view()),
    
]