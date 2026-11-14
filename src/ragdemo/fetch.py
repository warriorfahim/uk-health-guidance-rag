"""Download public GOV.UK guidance pages as plain text into data/raw/.

Uses two free, no-key GOV.UK APIs (standard library only, no extra installs):
  * Search API  https://www.gov.uk/api/search.json   -> find candidate pages
  * Content API https://www.gov.uk/api/content/<path> -> get each page's HTML body

Content is Crown copyright under the Open Government Licence v3.0 unless stated otherwise.
The Content API allows 10 requests per second per client; this script stays well below that.

Usage:
  python -m ragdemo.fetch discover            # writes candidate paths to data/sources.txt
  # edit data/sources.txt: keep the 20-40 pages you want, delete the rest
  python -m ragdemo.fetch fetch               # writes data/raw/<slug>.txt and data/raw/manifest.csv
"""
import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://www.gov.uk"
USER_AGENT = "uk-health-guidance-rag-demo/0.1 (personal portfolio project)"
BLOCK_TAGS = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "br", "table", "section"}
SKIP_TAGS = {"script", "style", "nav", "footer"}


class _TextExtractor(HTMLParser):
    """Turn GOV.UK body HTML into readable text, one heading or list item per line."""

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self._skip += 1
        elif tag in {"h2", "h3", "h4"}:
            self.parts.append("\n\n## ")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag in BLOCK_TAGS:
            self.parts.append("\n")
        elif tag in {"td", "th"}:
            self.parts.append(" | ")

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self._skip:
            self._skip -= 1
        elif tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def html_to_text(html: str) -> str:
    parser = _TextExtractor()
    parser.feed(html)
    text = "".join(parser.parts)
    text = re.sub(r"[ \t\xa0]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_body(item: dict) -> str:
    """Return the page's main HTML from a Content API item, or '' if it has none.

    detailed_guide / html_publication / answer pages keep it in details.body;
    mainstream multi-part guides keep it in details.parts[].body.
    """
    details = item.get("details", {})
    body = details.get("body")
    if isinstance(body, list):  # some schemas return [{"content_type": ..., "content": ...}]
        body = next(
            (b.get("content", "") for b in body if b.get("content_type") == "text/html"), ""
        )
    if body:
        return body
    parts = details.get("parts") or []
    return "\n".join(f"<h2>{p.get('title', '')}</h2>{p.get('body', '')}" for p in parts)


def slugify(path: str) -> str:
    slug = path.strip("/").split("/")[-1]
    return re.sub(r"[^a-z0-9-]+", "-", slug.lower()).strip("-")[:80] or "page"


def _get_json(url: str) -> dict:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def discover(org: str, doc_types: list[str], query: str, count: int, out_path: Path) -> None:
    params = [("filter_organisations", org), ("count", str(count)),
              ("fields", "link"), ("fields", "title"), ("order", "-public_timestamp")]
    params += [("filter_content_store_document_type", t) for t in doc_types]
    if query:
        params.append(("q", query))
    url = f"{BASE}/api/search.json?{urllib.parse.urlencode(params)}"
    results = _get_json(url).get("results", [])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# One GOV.UK path per line. Delete the ones you don't want.\n")
        f.write("# Anything after a # is ignored.\n")
        f.writelines(f"{r['link']}    # {r.get('title', '')}\n" for r in results)
    print(f"Wrote {len(results)} candidate paths to {out_path}")


def read_paths(sources_path: Path) -> list[str]:
    paths = []
    for line in sources_path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            paths.append(urllib.parse.urlparse(line).path if line.startswith("http") else line)
    return paths


def fetch(sources_path: Path, raw_dir: Path, delay: float = 0.3, min_words: int = 100) -> None:
    raw_dir.mkdir(parents=True, exist_ok=True)
    rows, skipped = [], []
    for path in read_paths(sources_path):
        try:
            item = _get_json(f"{BASE}/api/content{path}")
        except (OSError, ValueError) as exc:  # network error, HTTP 404, bad JSON
            skipped.append((path, str(exc)))
            continue
        text = html_to_text(extract_body(item))
        if len(text.split()) < min_words:
            words = len(text.split())
            skipped.append((path, f"only {words} words (probably a PDF-only or collection page)"))
            continue
        name = f"{slugify(path)}.txt"
        title = item.get("title", "")
        (raw_dir / name).write_text(f"{title}\n\n{text}\n", encoding="utf-8")
        rows.append({"source": name, "title": title, "url": BASE + path,
                     "updated": item.get("public_updated_at", ""), "licence": "OGL v3.0"})
        print(f"saved {name} ({len(text.split())} words)")
        time.sleep(delay)
    with open(raw_dir / "manifest.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "title", "url", "updated", "licence"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved {len(rows)} pages to {raw_dir}; skipped {len(skipped)}.")
    for path, reason in skipped:
        print(f"  skipped {path}: {reason}")


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("discover", help="list candidate pages via the GOV.UK Search API")
    d.add_argument("--org", default="uk-health-security-agency")
    d.add_argument("--doc-type", action="append", dest="doc_types",
                   help="content_store_document_type, repeatable (default: detailed_guide)")
    d.add_argument("--query", default="", help="optional keywords, e.g. 'vaccination'")
    d.add_argument("--count", type=int, default=100)
    d.add_argument("--out", default="data/sources.txt")
    f = sub.add_parser("fetch", help="download each path in sources.txt as plain text")
    f.add_argument("--sources", default="data/sources.txt")
    f.add_argument("--raw-dir", default="data/raw")
    args = ap.parse_args(argv)
    if args.cmd == "discover":
        doc_types = args.doc_types or ["detailed_guide"]
        discover(args.org, doc_types, args.query, args.count, Path(args.out))
    else:
        if not Path(args.sources).exists():
            sys.exit(f"{args.sources} not found. Run discover first or write the paths yourself.")
        fetch(Path(args.sources), Path(args.raw_dir))


if __name__ == "__main__":
    main()
