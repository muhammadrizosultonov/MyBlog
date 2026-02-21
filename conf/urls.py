from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.blog.feeds import LatestPostsFeed
from apps.blog.sitemaps import BlogSitemap
from apps.core.sitemaps import StaticViewSitemap
from apps.portfolio.sitemaps import ProjectSitemap
from apps.core import views as core_views

sitemaps = {
    "blog": BlogSitemap,
    "projects": ProjectSitemap,
    "static": StaticViewSitemap,
}

admin.site.site_header = "Muhammadrizo Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Dashboard"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("me.urls")),
    path("", include("apps.portfolio.urls")),
    path("", include("apps.blog.urls")),
    path("", include("apps.ai.urls")),
    path("markdownx/", include("markdownx.urls")),
    path("rss/", LatestPostsFeed(), name="rss_feed"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", core_views.robots_txt, name="robots_txt"),
]

handler404 = "apps.core.views.custom_404"
handler500 = "apps.core.views.custom_500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
