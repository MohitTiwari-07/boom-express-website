import re
from django import template
from django.utils.html import format_html, format_html_join

register = template.Library()

@register.filter
def format_article(value):
    paragraphs = [p.strip() for p in (value or "").split("\n\n") if p.strip()]
    rendered = []

    for paragraph in paragraphs:
        paragraph = " ".join(line.strip() for line in paragraph.splitlines()).strip()
        is_numbered = bool(re.match(r"^\d+\.\s+", paragraph))
        is_final = paragraph.upper().rstrip(":") == "FINAL THOUGHT"
        is_heading = (
            len(paragraph) <= 85
            and paragraph == paragraph.upper()
            and any(char.isalpha() for char in paragraph)
        )

        if is_numbered or is_final or is_heading:
            rendered.append(format_html(
                '<h2 class="article-subheading">{}</h2>', paragraph
            ))
        else:
            rendered.append(format_html("<p>{}</p>", paragraph))

    return format_html_join("\n", "{}", ((item,) for item in rendered))
