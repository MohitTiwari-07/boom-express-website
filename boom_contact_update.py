from pathlib import Path
from datetime import datetime
import os, json, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import CompanyProfile

profile, created = CompanyProfile.objects.get_or_create(pk=1)

backup_dir = Path("backups") / ("boom_contact_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
backup_dir.mkdir(parents=True, exist_ok=True)

before = {f.name: str(getattr(profile, f.name, "")) for f in profile._meta.fields}
(backup_dir / "company_profile_before.json").write_text(
    json.dumps(before, indent=2, ensure_ascii=False), encoding="utf-8"
)

verified = {
    "company_name": "BOOM EXPRESS TECHNICAL SERVICES L.L.C.",
    "phone": "+971 52 512 2024",
    "email": "jhuriyanarendra15@gmail.com",
    "address": "Office A18-01-1, Oud Metha, Bur Dubai, Dubai, UAE",
}

updated = []
for field, value in verified.items():
    if field in [f.name for f in profile._meta.fields]:
        setattr(profile, field, value)
        updated.append(field)

if "updated_at" in [f.name for f in profile._meta.fields]:
    updated.append("updated_at")

profile.save(update_fields=list(dict.fromkeys(updated)))

print("BACKUP:", backup_dir)
print("UPDATED FIELDS:", updated)
print("COMPANY:", profile.company_name)
print("PHONE:", getattr(profile, "phone", "FIELD MISSING"))
print("EMAIL:", getattr(profile, "email", "FIELD MISSING"))
print("ADDRESS:", getattr(profile, "address", "FIELD MISSING"))
print("WHATSAPP PRESERVED:", getattr(profile, "whatsapp", "FIELD MISSING"))
