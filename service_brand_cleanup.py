from pathlib import Path
from datetime import datetime
import os, json, re, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import Service

root = Path.cwd()
backup_dir = root / "backups" / ("service_db_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
backup_dir.mkdir(parents=True, exist_ok=True)

records = list(Service.objects.all().values())
(backup_dir / "services_before.json").write_text(
    json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
)

fields = ["short_description", "description", "meta_title", "meta_description"]
updated = 0

for service in Service.objects.all():
    changed_fields = []
    for field in fields:
        value = getattr(service, field, "") or ""
        new_value = re.sub(r"NEXORA", "BOOM EXPRESS", value, flags=re.I)
        if new_value != value:
            setattr(service, field, new_value)
            changed_fields.append(field)
    if changed_fields:
        service.save(update_fields=changed_fields)
        updated += 1

print("Backup:", backup_dir)
print("Service records updated:", updated)
print("Total services:", Service.objects.count())
print("Active services:", Service.objects.filter(is_active=True).count())
print("Remaining NEXORA in service content:", sum(
    1 for s in Service.objects.all()
    for f in fields
    if "NEXORA" in (getattr(s, f, "") or "").upper()
))
print("\nHOMEPAGE SERVICE ORDER:")
for s in Service.objects.filter(is_active=True).order_by("order", "title")[:5]:
    print(s.order, s.title, "->", s.slug)
