from pathlib import Path

path = Path("templates/base.html")
content = path.read_text(encoding="utf-8")

replacements = [
(
    '<title>{% block title %}NEXORA | Premium Technical Services{% endblock %}</title>',
    '<title>{% block title %}{{ site_company_name }} | Premium Technical Services{% endblock %}</title>'
),
(
    '<meta name="description" content="{% block meta_description %}NEXORA delivers professional technical and property improvement services with precision, thoughtful execution and attention to detail.{% endblock %}">',
    '<meta name="description" content="{% block meta_description %}{{ company_profile.meta_description|default:company_profile.tagline|default:\'Professional technical services and property improvement solutions.\' }}{% endblock %}">'
),
(
    '<meta property="og:site_name" content="NEXORA Technical Services">',
    '<meta property="og:site_name" content="{{ site_company_name }}">'
),
(
    '<meta property="og:title" content="{% block og_title %}NEXORA | Premium Technical Services{% endblock %}">',
    '<meta property="og:title" content="{% block og_title %}{{ site_company_name }} | Premium Technical Services{% endblock %}">'
),
(
    '<meta name="twitter:title" content="{% block twitter_title %}NEXORA | Premium Technical Services{% endblock %}">',
    '<meta name="twitter:title" content="{% block twitter_title %}{{ site_company_name }} | Premium Technical Services{% endblock %}">'
),
(
    '<link rel="icon" type="image/svg+xml" href="{% static \'images/favicon.svg\' %}">\n    <link rel="alternate icon" href="{% static \'images/favicon.svg\' %}">',
    '{% if company_profile and company_profile.favicon %}\n    <link rel="icon" href="{{ company_profile.favicon.url }}">\n    {% else %}\n    <link rel="icon" type="image/svg+xml" href="{% static \'images/favicon.svg\' %}">\n    <link rel="alternate icon" href="{% static \'images/favicon.svg\' %}">\n    {% endif %}'
),
(
    '"name": "NEXORA Technical Services",',
    '"name": "{{ site_company_name|escapejs }}",'
),
(
    '<span class="brand-mark">N</span>\n                    <span class="brand-copy">\n                        <strong>EXORA</strong>\n                        <small>TECHNICAL SERVICES</small>\n                    </span>',
    '{% if company_profile and company_profile.logo %}\n                    <img src="{{ company_profile.logo.url }}" alt="{{ site_company_name }}" style="max-height:46px;width:auto;">\n                    {% else %}\n                    <span class="brand-mark">{{ site_company_name|slice:":1" }}</span>\n                    <span class="brand-copy">\n                        <strong>{{ site_company_name }}</strong>\n                        <small>{% if company_profile and company_profile.tagline %}{{ company_profile.tagline }}{% else %}TECHNICAL SERVICES{% endif %}</small>\n                    </span>\n                    {% endif %}'
),
(
    '<span class="brand-mark">N</span>\n                            <span class="brand-copy">\n                                <strong>EXORA</strong>\n                                <small>TECHNICAL SERVICES</small>\n                            </span>',
    '{% if company_profile and company_profile.logo %}\n                            <img src="{{ company_profile.logo.url }}" alt="{{ site_company_name }}" style="max-height:46px;width:auto;">\n                            {% else %}\n                            <span class="brand-mark">{{ site_company_name|slice:":1" }}</span>\n                            <span class="brand-copy">\n                                <strong>{{ site_company_name }}</strong>\n                                <small>{% if company_profile and company_profile.tagline %}{{ company_profile.tagline }}{% else %}TECHNICAL SERVICES{% endif %}</small>\n                            </span>\n                            {% endif %}'
),
(
    'Thoughtful technical solutions, precise workmanship\n                            and a commitment to quality in every detail.',
    '{{ company_profile.footer_text|default:"Thoughtful technical solutions, precise workmanship and a commitment to quality in every detail." }}'
),
(
    '<a href="{% url \'core:home\' %}#why-us">Why NEXORA</a>',
    '<a href="{% url \'core:home\' %}#why-us">Why Choose Us</a>'
),
(
    '<p>Have a project in mind?</p>',
    '<p>{% if company_profile and company_profile.phone %}{{ company_profile.phone }}{% else %}Have a project in mind?{% endif %}</p>\n                        {% if company_profile and company_profile.email %}<a href="mailto:{{ company_profile.email }}">{{ company_profile.email }}</a>{% endif %}'
),
(
    '<p>Â© {% now "Y" %} NEXORA Technical Services. All rights reserved.</p>',
    '<p>&copy; {% now "Y" %} {{ site_company_name }}. All rights reserved.</p>'
),
]

for old, new in replacements:
    count = content.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one match, found {count}: {old[:100]}")
    content = content.replace(old, new, 1)

path.write_text(content, encoding="utf-8")
print("Updated base.html successfully.")
