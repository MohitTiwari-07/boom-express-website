from pathlib import Path
import re

# Remove only the team photo element
p = Path("templates/home.html")
s = p.read_text(encoding="utf-8")

pattern = r'        <div class="boom-team-image">\s*<img src="\{% static \'images/boom-express-technicians\.webp\' %\}"\s*alt="BOOM EXPRESS technical services team"\s*loading="lazy" decoding="async" width="1672"\s*height="941">\s*</div>\s*'
s, count = re.subn(pattern, "", s, count=1)

if count != 1:
    raise SystemExit("Team photo block not matched. No HTML saved.")

p.write_text(s, encoding="utf-8")

# Compact spacing, only for this section
css = Path("static/css/style.css")
c = css.read_text(encoding="utf-8")

c += """

/* Compact BOOM EXPRESS text section - photo removed */
.boom-team-section {
    padding-top: clamp(28px, 3vw, 42px);
    padding-bottom: clamp(28px, 3vw, 42px);
}
.boom-team-grid {
    grid-template-columns: minmax(0, 1fr);
    gap: 0;
    max-width: 900px;
}
.boom-team-image {
    display: none;
}
.boom-team-copy .section-title {
    margin: 8px 0 12px;
}
.boom-team-copy .section-description {
    margin-bottom: 16px;
}
"""

css.write_text(c, encoding="utf-8")
print("Homepage team photo removed; section spacing reduced.")
