from pathlib import Path
from datetime import datetime
import shutil

root = Path.cwd()
files = [
    root / "templates" / "contact.html",
    root / "templates" / "base.html",
    root / "static" / "css" / "style.css",
]

backup = root / "backups" / ("contact_display_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
backup.mkdir(parents=True, exist_ok=True)

for f in files:
    if not f.exists():
        raise SystemExit(f"Missing file: {f}")

# Backup before editing
for f in files:
    dest = backup / f.relative_to(root)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(f, dest)

# CONTACT PAGE
p = files[0]
s = p.read_text(encoding="utf-8")
anchor = '<p>Share your technical requirements or project enquiry using the form. Our team can review the information you provide.</p>'
contact_html = '''<p>Share your technical requirements or project enquiry using the form. Our team can review the information you provide.</p>

            <div class="company-contact-details">
                {% if company_profile.phone %}
                <div class="company-contact-item">
                    <span class="contact-detail-label">CALL US</span>
                    <a href="tel:{{ company_profile.phone|cut:' ' }}">{{ company_profile.phone }}</a>
                </div>
                {% endif %}
                {% if company_profile.email %}
                <div class="company-contact-item">
                    <span class="contact-detail-label">EMAIL US</span>
                    <a href="mailto:{{ company_profile.email }}">{{ company_profile.email }}</a>
                </div>
                {% endif %}
                {% if company_profile.address %}
                <div class="company-contact-item">
                    <span class="contact-detail-label">OUR OFFICE</span>
                    <p>{{ company_profile.address }}</p>
                </div>
                {% endif %}
            </div>'''
if s.count(anchor) != 1:
    raise SystemExit("Contact page insertion point not found exactly once. No edits applied.")
p.write_text(s.replace(anchor, contact_html), encoding="utf-8")

# FOOTER CONTACT
p = files[1]
s = p.read_text(encoding="utf-8")
old = '''                    <div class="footer-column footer-contact">
                        <h3>Get in Touch</h3>
                        <p>Have a project in mind?</p>
                        <a href="{% url 'core:home' %}#contact" class="footer-email">
                            Start a Conversation ↗
                        </a>
                    </div>'''
new = '''                    <div class="footer-column footer-contact">
                        <h3>Get in Touch</h3>
                        <p>Have a project in mind?</p>
                        {% if company_profile.phone %}
                        <a href="tel:{{ company_profile.phone|cut:' ' }}" class="footer-email">{{ company_profile.phone }}</a>
                        {% endif %}
                        {% if company_profile.email %}
                        <a href="mailto:{{ company_profile.email }}" class="footer-email">{{ company_profile.email }}</a>
                        {% endif %}
                        {% if company_profile.address %}
                        <p>{{ company_profile.address }}</p>
                        {% endif %}
                        <a href="{% url 'core:contact' %}" class="footer-email">
                            Send an Enquiry ↗
                        </a>
                    </div>'''
if s.count(old) != 1:
    raise SystemExit("Footer insertion point not found exactly once. Contact page was updated; restore from backup before retrying.")
p.write_text(s.replace(old, new), encoding="utf-8")

# CONTACT DETAILS STYLING
p = files[2]
css = p.read_text(encoding="utf-8")
css_add = '''

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
'''
if "/* BOOM EXPRESS contact details */" not in css:
    p.write_text(css.rstrip() + "\n" + css_add, encoding="utf-8")

print("Contact page, footer and styling updated.")
print("Backup:", backup)
