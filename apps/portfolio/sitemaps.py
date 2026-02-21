from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Project.objects.all()

    def location(self, obj):
        return reverse("project_detail", args=[obj.slug])
