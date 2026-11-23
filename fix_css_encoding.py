from pathlib import Path
from datetime import datetime
import shutil

p = Path("static/css/style.css")
backup = Path("backups") / ("style_css_encoding_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
backup.mkdir(parents=True, exist_ok=True)
shutil.copy2(p, backup / "style.css")

# Original CSS encoding is Windows-1252; preserve existing content.
css = p.read_text(encoding="cp1252")

css_add = """

/* BOOM EXPRESS contact details */
.company-contact-details {
    display: grid;
    gap: 18px;
    margin-top: 30px;
}
.company-contact-item {
    padding: 16px 18px;
    border: 1px solid rgba(190, 157, 98, 0.28);
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.025);
}
.contact-detail-label {
    display: block;
    margin-bottom: 7px;
    color: #b99a62;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
}
.company-contact-item a,
.company-contact-item p {
    margin: 0;
    color: inherit;
    overflow-wrap: anywhere;
    text-decoration: none;
}
.company-contact-item a:hover {
    color: #c5a66c;
}
.footer-contact a {
    display: block;
    overflow-wrap: anywhere;
}
"""

if "/* BOOM EXPRESS contact details */" not in css:
    css += css_add

p.write_text(css, encoding="utf-8")
print("CSS encoding converted to UTF-8; existing CSS preserved.")
print("Backup:", backup)
