
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),

    path("services/", views.services, name="services"),
    path(
        "services/<slug:slug>/",
        views.service_detail,
        name="service_detail"
    ),

    path("industries/", views.industries, name="industries"),

    path("projects/", views.projects, name="projects"),
    path(
        "projects/<slug:slug>/",
        views.project_detail,
        name="project_detail"
    ),

    path("insights/", views.blog_list, name="blog_list"),
    path(
        "insights/<slug:slug>/",
        views.blog_detail,
        name="blog_detail"
    ),

    path("faqs/", views.faqs, name="faqs"),
    path("contact/", views.contact, name="contact"),
    path(
        "contact/submit/",
        views.submit_enquiry,
        name="submit_enquiry"
    ),
]
