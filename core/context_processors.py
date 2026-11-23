from .models import CompanyProfile


def company_profile(request):
    profile = CompanyProfile.objects.first()
    return {
        "company_profile": profile,
        "site_company_name": (
            profile.company_name
            if profile and profile.company_name
            else "BOOM EXPRESS TECHNICAL SERVICES L.L.C."
        ),
    }
