from django.urls import path
from .views import PostListAPIView

urlpatterns = [
    path("api/posts/", PostListAPIView.as_view(), name="api_posts"),
]
