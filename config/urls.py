
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse

from core.sitemaps import (
    StaticViewSitemap,
    ServiceSitemap,
    ProjectSitemap,
    BlogSitemap,
)

sitemaps = {
    "static": StaticViewSitemap,
    "services": ServiceSitemap,
    "projects": ProjectSitemap,
    "blogs": BlogSitemap,
}


def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        f"Sitemap: {settings.SITE_URL.rstrip('/')}/sitemap.xml\n"
    )
    return HttpResponse(content, content_type="text/plain")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
