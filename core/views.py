from django.views.decorators.csrf import ensure_csrf_cookie

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import Service, Industry, Project, BlogPost, FAQ
from .forms import EnquiryForm


def home(request):
    context = {
        "services": Service.objects.filter(is_active=True).order_by("order", "title")[:5],
        "industries": Industry.objects.filter(is_active=True),
        "projects": Project.objects.filter(
            is_published=True, is_featured=True
        )[:6],
        "latest_blogs": BlogPost.objects.filter(
            is_published=True
        )[:3],
        "enquiry_form": EnquiryForm(),
    }
    return render(request, "home.html", context)


def about(request):
    return render(request, "about.html")


def services(request):
    service_list = Service.objects.filter(is_active=True).order_by("order", "title")
    return render(request, "services.html", {"services": service_list})


def service_detail(request, slug):
    service = get_object_or_404(
        Service, slug=slug, is_active=True
    )
    related_services = Service.objects.filter(
        is_active=True
    ).exclude(pk=service.pk).order_by("order", "title")

    return render(request, "service_detail.html", {
        "service": service,
        "related_services": related_services,
    })

def industries(request):
    industry_list = Industry.objects.filter(is_active=True)
    return render(
        request, "industries.html", {"industries": industry_list}
    )


def projects(request):
    project_list = Project.objects.filter(is_published=True)
    return render(request, "projects.html", {"projects": project_list})


def project_detail(request, slug):
    project = get_object_or_404(
        Project, slug=slug, is_published=True
    )
    return render(
        request, "project_detail.html", {"project": project}
    )


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, "blog_list.html", {"posts": posts})


def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost, slug=slug, is_published=True
    )
    return render(request, "blog_detail.html", {"post": post})


def faqs(request):
    faq_list = FAQ.objects.filter(is_active=True).select_related(
        "service"
    ).order_by("order", "question")
    return render(request, "faqs.html", {"faqs": faq_list})


@ensure_csrf_cookie
def contact(request):
    form = EnquiryForm()
    return render(request, "contact.html", {"form": form})


@require_POST
def submit_enquiry(request):
    form = EnquiryForm(request.POST)

    if not form.is_valid():
        messages.error(
            request, "Please check the form and correct the errors."
        )
        return render(
            request,
            "contact.html",
            {"form": form},
            status=400
        )

    enquiry = form.save()

    contact_email = getattr(settings, "CONTACT_EMAIL", "")

    if contact_email:
        try:
            send_mail(
                subject=f"Website enquiry: {enquiry.subject or 'New enquiry'}",
                message=(
                    f"Name: {enquiry.name}\n"
                    f"Email: {enquiry.email}\n"
                    f"Phone: {enquiry.phone}\n\n"
                    f"Message:\n{enquiry.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact_email],
                fail_silently=True,
            )
        except Exception:
            pass

    messages.success(
        request,
        "Thank you. Your enquiry has been received successfully."
    )
    return redirect("core:contact")

