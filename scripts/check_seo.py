#!/usr/bin/env python3
"""Check the static site's crawlability with only the Python standard library.

Run from any directory: python scripts/check_seo.py
"""

import json
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://" + (ROOT / "CNAME").read_text().strip()
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9",
      "x": "http://www.w3.org/1999/xhtml"}


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        relative = path.relative_to(ROOT).as_posix()
        self.url = ORIGIN + "/" + relative.removesuffix("index.html")
        self.tags = []
        self.json_documents = []
        self.json_errors = []
        self.json_text = None
        self.title_parts = []
        self.in_title = False
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "title":
            self.in_title = True
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.json_text = ""

    def handle_data(self, text):
        if self.in_title:
            self.title_parts.append(text)
        if self.json_text is not None:
            self.json_text += text

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "script" and self.json_text is not None:
            try:
                self.json_documents.append(json.loads(self.json_text))
            except json.JSONDecodeError as error:
                self.json_errors.append(str(error))
            self.json_text = None

    def meta(self, key):
        return [attrs.get("content", "") for tag, attrs in self.tags
                if tag == "meta" and attrs.get("name", attrs.get("property")) == key]

    def links(self, relation):
        return [attrs for tag, attrs in self.tags
                if tag == "link" and relation in attrs.get("rel", "").split()]

    def alternates(self):
        return {link["hreflang"]: link.get("href", "")
                for link in self.links("alternate") if "hreflang" in link}


def local_file(url):
    parsed = urlsplit(url)
    if parsed.scheme not in ("http", "https") or parsed.netloc != urlsplit(ORIGIN).netloc:
        return None
    path = ROOT / unquote(parsed.path.lstrip("/"))
    return path / "index.html" if path.is_dir() else path


def main():
    errors = []

    def check(condition, source, message):
        if not condition:
            errors.append(f"{source}: {message}")

    pages = {}
    for path in sorted(ROOT.rglob("*.html")):
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        page = Page(path)
        # Search-engine verification files are plain text, not HTML pages.
        if any(tag == "html" for tag, _ in page.tags):
            pages[page.url] = page

    sitemap = ET.parse(ROOT / "sitemap.xml")
    entries = sitemap.findall("s:url", NS)
    urls = [entry.findtext("s:loc", namespaces=NS) for entry in entries]
    check(len(urls) == len(set(urls)), "sitemap.xml", "duplicate URLs")
    sitemap_urls = set(urls)
    titles = Counter()

    for url, page in pages.items():
        source = page.path.relative_to(ROOT)
        for error in page.json_errors:
            check(False, source, "invalid JSON-LD: " + error)
        for tag, attrs in page.tags:
            refs = []
            if tag in ("a", "link"):
                refs.append(attrs.get("href"))
            if tag in ("img", "script", "source"):
                refs.append(attrs.get("src"))
            if tag == "video":
                refs.append(attrs.get("poster"))
            for ref in filter(None, refs):
                target = local_file(urljoin(url, ref))
                check(target is None or target.is_file(), source, f"missing local target: {ref}")
            if tag == "img":
                check("alt" in attrs, source, "image is missing alt text")
                check(all(attrs.get(key, "").isdigit() and int(attrs[key]) > 0
                          for key in ("width", "height")), source,
                      f"image needs positive width and height: {attrs.get('src')}")

        robots = ",".join(page.meta("robots")).lower().replace(",", " ").split()
        if "noindex" in robots:
            check(url not in sitemap_urls, source, "noindex page is listed in the sitemap")
            continue
        canonical = page.links("canonical")
        check(len(canonical) == 1 and canonical[0].get("href") == url,
              source, "expected one self-referencing canonical: " + url)
        check(url in sitemap_urls, source, "indexable page missing from sitemap")
        check(sum(tag == "title" for tag, _ in page.tags) == 1 and bool(page.title_parts),
              source, "expected one nonempty title")
        titles["".join(page.title_parts)] += 1
        check(sum(tag == "h1" for tag, _ in page.tags) == 1, source, "expected one h1")
        check(len(page.meta("description")) == 1 and bool(page.meta("description")[0]),
              source, "expected one nonempty meta description")
        check(any(tag == "html" and attrs.get("lang") for tag, attrs in page.tags),
              source, "missing document language")
        if page.meta("og:type"):
            for key in ("og:title", "og:description", "og:image", "twitter:card", "twitter:image"):
                check(len(page.meta(key)) == 1 and bool(page.meta(key)[0]), source, f"missing or duplicate {key}")
            check(page.meta("og:url") == [url], source, "og:url differs from canonical")
            for key in ("og:image", "twitter:image"):
                for image in page.meta(key):
                    target = local_file(image)
                    check(image.startswith(ORIGIN + "/") and target is not None and target.is_file(),
                          source, f"missing absolute local share image: {image}")

        alternates = page.alternates()
        if alternates:
            check(url in alternates.values(), source, "hreflang must include this page")
        for language, target in alternates.items():
            check(target in pages and pages[target].alternates() == alternates,
                  source, f"missing or nonreciprocal hreflang: {language} {target}")

    for title, count in titles.items():
        check(count == 1, "titles", f"duplicate title ({count} pages): {title}")
    for entry in entries:
        url = entry.findtext("s:loc", namespaces=NS)
        check(url in pages, "sitemap.xml", f"URL has no HTML page: {url}")
        if url in pages:
            alternates = {link.get("hreflang"): link.get("href") for link in entry.findall("x:link", NS)}
            check(alternates == pages[url].alternates(), "sitemap.xml", f"hreflang differs from HTML: {url}")
    check(f"Sitemap: {ORIGIN}/sitemap.xml" in (ROOT / "robots.txt").read_text(),
          "robots.txt", "missing sitemap declaration")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"SEO checks passed: {len(pages)} HTML pages, {len(entries)} sitemap URLs; "
          "canonical, metadata, JSON-LD, hreflang, local links and images verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
