import re
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

base = "http://127.0.0.1:8000"
pages = [
    "/", "/about/", "/services/", "/industries/",
    "/projects/", "/insights/", "/faqs/", "/contact/"
]

checked = set()
broken = []

for page in pages:
    try:
        req = Request(base + page, headers={"User-Agent": "Mozilla/5.0"})
        html = urlopen(req, timeout=10).read().decode("utf-8", "replace")
    except Exception as e:
        print("PAGE ERROR:", page, e)
        continue

    for href in re.findall(r'''href=["']([^"'#]+)''', html):
        url = urljoin(base + page, href)
        parsed = urlparse(url)

        if parsed.netloc != urlparse(base).netloc:
            continue

        path = parsed.path
        if not path or path.startswith(("/static/", "/media/", "/admin/")):
            continue

        if url in checked:
            continue
        checked.add(url)

        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=10) as response:
                if response.status >= 400:
                    broken.append((response.status, path))
        except HTTPError as e:
            broken.append((e.code, path))
        except URLError as e:
            broken.append(("ERROR", path))

print("\nInternal URLs checked:", len(checked))
print("Broken URLs:", len(broken))
for item in broken:
    print(item)
