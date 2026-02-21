from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("projects/", views.projects_view, name="projects"),
    path("projects/<slug:slug>/", views.project_detail_view, name="project_detail"),
    path("blog/", views.blog_view, name="blog"),
    path("blog/<slug:slug>/", views.blog_detail_view, name="blog_detail"),
    path("contact/", views.contact_view, name="contact"),
]
