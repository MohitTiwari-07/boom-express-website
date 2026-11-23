from pathlib import Path
from datetime import datetime
import shutil, re

home = Path("templates/home.html")
css = Path("static/css/style.css")
img = Path("static/images/boom-express-technicians.webp")

if not home.exists() or not css.exists() or not img.exists():
    raise SystemExit("Required homepage, CSS or image file missing.")

backup = Path("backups") / ("team_section_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(home, backup / "home.html")
shutil.copy2(css, backup / "style.css")

html = home.read_text(encoding="utf-8")
styles = css.read_text(encoding="utf-8")

if "boom-team-section" in html:
    print("Team section already exists; no duplicate added.")
else:
    match = re.search(r'<section\b[^>]*\bid=["\']projects["\'][^>]*>', html, re.I)
    if not match:
        match = re.search(r'<section\b[^>]*>[\s\S]{0,500}?Our Selected Projects', html, re.I)
    if not match:
        raise SystemExit("Projects section not located. No template changes made.")

    if "{% load static %}" not in html:
        extends = re.search(r'{%\s*extends\s+[^%]+%}', html)
        if extends:
            html = html[:extends.end()] + "\n{% load static %}" + html[extends.end():]
        else:
            html = "{% load static %}\n" + html

    section = '''
<!-- BOOM EXPRESS TEAM -->
<section class="section boom-team-section">
    <div class="container boom-team-grid">
        <div class="boom-team-image">
            <img src="{% static 'images/boom-express-technicians.webp' %}"
                 alt="BOOM EXPRESS technical services team"
                 loading="lazy" decoding="async" width="1672" height="941">
        </div>
        <div class="boom-team-copy">
            <span class="eyebrow">The People Behind The Work</span>
            <h2 class="section-title">Professional Service.<br><span>Quality That Shows.</span></h2>
            <p class="section-description">
                A professional approach to technical services, maintenance
                and finishing works, with attention to detail at every stage.
            </p>
            <a href="{% url 'core:contact' %}" class="btn btn-outline">
                Discuss Your Project <span>↗</span>
            </a>
        </div>
    </div>
</section>

'''
    html = html[:match.start()] + section + html[match.start():]
    home.write_text(html, encoding="utf-8")
    print("Team section added to homepage.")

if "/* BOOM EXPRESS TEAM SECTION */" not in styles:
    styles += '''

/* BOOM EXPRESS TEAM SECTION */
.boom-team-grid {
    display: grid;
    grid-template-columns: 1.15fr .85fr;
    align-items: center;
    gap: clamp(30px, 6vw, 80px);
}
.boom-team-image {
    overflow: hidden;
    border: 1px solid rgba(196,154,85,.35);
    background: #102337;
}
.boom-team-image img {
    display: block;
    width: 100%;
    height: 100%;
    min-height: 340px;
    max-height: 510px;
    object-fit: cover;
}
.boom-team-copy .section-title {
    margin: 20px 0;
}
.boom-team-copy .section-description {
    margin-bottom: 28px;
}
@media(max-width: 768px) {
    .boom-team-grid { grid-template-columns: 1fr; gap: 28px; }
    .boom-team-image img { min-height: 230px; max-height: 340px; }
}
'''
    css.write_text(styles, encoding="utf-8")
    print("Responsive team styling added.")

print("Backup:", backup)
