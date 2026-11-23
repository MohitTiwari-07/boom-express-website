from django.contrib import admin
from .models import (
    Service, Industry, Project, BlogPost, Enquiry,
    CompanyProfile, FAQ, ServiceGallery, ServiceFeature, PageContent
)


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Company Identity", {"fields": ("company_name", "tagline", "logo", "favicon")}),
        ("Contact Information", {"fields": ("phone", "whatsapp", "email", "address", "map_url", "opening_hours")}),
        ("Social Media", {"fields": ("instagram_url", "facebook_url", "linkedin_url", "youtube_url")}),
        ("Website SEO", {"fields": ("meta_title", "meta_description")}),
        ("Footer", {"fields": ("footer_text",)}),
    )
    readonly_fields = ("updated_at",)
    def has_add_permission(self, request):
        return not CompanyProfile.objects.exists()


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "title")


@admin.register(ServiceGallery)
class ServiceGalleryAdmin(admin.ModelAdmin):
    list_display = ("service", "caption", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("service", "is_active")
    search_fields = ("service__title", "caption", "alt_text")


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "service", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("service", "is_active")
    search_fields = ("title", "description", "service__title")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "service", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("category", "service", "is_active")
    search_fields = ("question", "answer")


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ("page_name", "section_name", "heading", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("page_name", "is_active")
    search_fields = ("key", "page_name", "section_name", "heading", "content")


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")
    ordering = ("order", "title")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "location", "is_featured", "is_published")
    list_editable = ("is_featured", "is_published")
    list_filter = ("category", "is_featured", "is_published")
    search_fields = ("title", "category", "location")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "-completion_date")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "is_published")
    list_editable = ("is_published",)
    list_filter = ("is_published", "published_at")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "service", "created_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "phone", "service", "subject", "message")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
