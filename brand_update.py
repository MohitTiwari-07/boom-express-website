from pathlib import Path
import re, shutil

root = Path.cwd()
targets = []
for folder in ["templates", "core", "config", "static"]:
    p = root / folder
    if p.exists():
        targets += [f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in {".html",".py",".css",".js",".txt",".xml"} and ".bak" not in f.name and "__pycache__" not in f.parts]

env = root / ".env"
if env.exists():
    targets.append(env)

backup = root / r"backups\boom_brand_20261121_160134"
backup.mkdir(parents=True, exist_ok=True)

changed = 0
for f in targets:
    try:
        original = f.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    updated = re.sub("NEXORA", "BOOM EXPRESS", original, flags=re.I)
    updated = updated.replace('<span class="brand-mark">N</span>', '<span class="brand-mark">B</span>')
    updated = updated.replace("<strong>EXORA</strong>", "<strong>OOM EXPRESS</strong>")
    if updated != original:
        dest = backup / f.relative_to(root)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest)
        f.write_text(updated, encoding="utf-8")
        changed += 1

print("Branding files updated:", changed)

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from core.models import CompanyProfile
profile, created = CompanyProfile.objects.get_or_create(pk=1)
profile.company_name = "BOOM EXPRESS TECHNICAL SERVICES L.L.C."
profile.save(update_fields=["company_name", "updated_at"])
print("Company profile:", profile.company_name)

