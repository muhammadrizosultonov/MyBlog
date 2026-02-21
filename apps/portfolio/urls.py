from django.urls import path
from .views import ProjectListAPIView

urlpatterns = [
    path("api/projects/", ProjectListAPIView.as_view(), name="api_projects"),
]
