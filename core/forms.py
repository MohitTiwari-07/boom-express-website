from django import forms
from .models import Enquiry, Service


class EnquiryForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput())

    service = forms.ChoiceField(
        required=False,
        label="Select a Service",
        choices=[("", "Choose a service (optional)")],
    )

    class Meta:
        model = Enquiry
        fields = ["name", "email", "phone", "service", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your full name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Your email address", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"placeholder": "Your phone number", "autocomplete": "tel"}),
            "subject": forms.TextInput(attrs={"placeholder": "How can we help?"}),
            "message": forms.Textarea(attrs={"placeholder": "Tell us about your requirements...", "rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        services = Service.objects.filter(is_active=True).order_by("order", "title")
        choices = [("", "Choose a service (optional)")]
        choices.extend((item.title, item.title) for item in services)
        choices.append(("Other / General Enquiry", "Other / General Enquiry"))
        self.fields["service"].choices = choices

    def clean_website(self):
        website = self.cleaned_data.get("website")
        if website:
            raise forms.ValidationError("Invalid submission.")
        return website

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name
