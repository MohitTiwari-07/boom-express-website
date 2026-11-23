
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Service, Project, BlogPost


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return [
            "core:home",
            "core:about",
            "core:services",
            "core:industries",
            "core:projects",
            "core:blog_list",
            "core:faqs",
            "core:contact",
        ]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Service.objects.filter(is_active=True)

    def location(self, item):
        return reverse("core:service_detail", args=[item.slug])


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Project.objects.filter(is_published=True)

    def location(self, item):
        return reverse("core:project_detail", args=[item.slug])


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def location(self, item):
        return reverse("core:blog_detail", args=[item.slug])
