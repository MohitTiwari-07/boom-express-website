
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True
    )
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Industry(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="industries/",
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=150, blank=True)
    summary = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True
    )
    location = models.CharField(max_length=200, blank=True)
    completion_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-completion_date", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=270, unique=True, blank=True)
    excerpt = models.CharField(max_length=400)
    content = models.TextField()
    cover_image = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True
    )
    published_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Enquiry(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    service = models.CharField(max_length=200, blank=True, default="")
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Customer Enquiry"
        verbose_name_plural = "Customer Enquiries"

    def __str__(self):
        return f"{self.name} — {self.created_at:%d %b %Y}"


class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=200, default="BOOM EXPRESS TECHNICAL SERVICES L.L.C.")
    tagline = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    map_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to="company/", blank=True, null=True)
    favicon = models.ImageField(upload_to="company/", blank=True, null=True)
    opening_hours = models.CharField(max_length=200, blank=True)
    footer_text = models.TextField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Profile"
        verbose_name_plural = "Company Profile"

    def __str__(self):
        return self.company_name


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ("general", "General"),
        ("services", "Services"),
        ("pricing", "Pricing"),
        ("process", "Process"),
        ("maintenance", "Maintenance"),
    ]

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="faqs",
    )
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="general",
    )
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "question"]
        verbose_name = "Frequently Asked Question"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class ServiceGallery(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="gallery_images",
    )
    image = models.ImageField(upload_to="services/gallery/")
    alt_text = models.CharField(max_length=250, blank=True)
    caption = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Service Gallery Image"
        verbose_name_plural = "Service Gallery"

    def __str__(self):
        return f"{self.service.title} - Image {self.pk or 'New'}"


class ServiceFeature(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="features",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Service Feature"
        verbose_name_plural = "Service Features"

    def __str__(self):
        return f"{self.service.title} - {self.title}"


class PageContent(models.Model):
    key = models.SlugField(max_length=100, unique=True)
    page_name = models.CharField(max_length=100)
    section_name = models.CharField(max_length=150)
    heading = models.CharField(max_length=250, blank=True)
    subheading = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="page-content/", blank=True, null=True)
    button_text = models.CharField(max_length=100, blank=True)
    button_url = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["page_name", "order"]
        verbose_name = "Page Content"
        verbose_name_plural = "Page Content"

    def __str__(self):
        return f"{self.page_name} - {self.section_name}"
