from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("blog_detail", args=[obj.slug])
