from django.urls import path
from . import views

app_name = "category"

urlpatterns = [
    path("", views.ListCreateView.as_view()),
    path("<int:pk>/", views.RetrieveUpdateView.as_view()),
    
]